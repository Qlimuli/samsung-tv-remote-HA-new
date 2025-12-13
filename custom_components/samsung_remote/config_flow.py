"""Config flow for Samsung TV Remote integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_NAME, CONF_SMARTTHINGS_ENTRY_ID
from .smartthings_bridge import SmartThingsBridge

_LOGGER = logging.getLogger(__name__)


async def _get_smartthings_entries(hass: HomeAssistant) -> list[config_entries.ConfigEntry]:
    """Get all SmartThings config entries."""
    return [
        entry
        for entry in hass.config_entries.async_entries("smartthings")
        if entry.state == config_entries.ConfigEntryState.LOADED
    ]


async def _get_samsung_tvs(hass: HomeAssistant, smartthings_entry: config_entries.ConfigEntry) -> list[dict[str, str]]:
    """Get Samsung TVs from SmartThings."""
    tvs = []
    
    # Access SmartThings data to get devices
    smartthings_data = hass.data.get("smartthings", {})
    
    # Try to get devices from the integration
    if smartthings_entry.entry_id in smartthings_data:
        entry_data = smartthings_data[smartthings_entry.entry_id]
        
        # Check for devices in broker
        if isinstance(entry_data, dict) and "broker" in entry_data:
            broker = entry_data["broker"]
            if hasattr(broker, "devices"):
                for device in broker.devices.values():
                    if _is_samsung_tv(device):
                        tvs.append({
                            "id": device.device_id,
                            "name": device.label or device.name,
                        })
    
    # Fallback: Check runtime_data
    if hasattr(smartthings_entry, "runtime_data"):
        runtime_data = smartthings_entry.runtime_data
        if hasattr(runtime_data, "devices"):
            for device in runtime_data.devices.values():
                if _is_samsung_tv(device):
                    if not any(tv["id"] == device.device_id for tv in tvs):
                        tvs.append({
                            "id": device.device_id,
                            "name": getattr(device, "label", None) or getattr(device, "name", "Samsung TV"),
                        })
    
    return tvs


def _is_samsung_tv(device: Any) -> bool:
    """Check if a device is a Samsung TV."""
    # Check device type
    device_type = getattr(device, "type", "").lower()
    if "tv" in device_type or "samsung" in device_type:
        return True
    
    # Check capabilities
    capabilities = getattr(device, "capabilities", [])
    if isinstance(capabilities, list):
        cap_names = [c.lower() if isinstance(c, str) else getattr(c, "id", "").lower() for c in capabilities]
        tv_capabilities = ["samsungvd.remotecontrol", "tvChannel", "mediaPlayback"]
        if any(cap in cap_names for cap in tv_capabilities):
            return True
    
    # Check OCF device type
    ocf_type = getattr(device, "ocf_device_type", "")
    if "tv" in ocf_type.lower():
        return True
    
    # Check device category
    category = getattr(device, "device_category", "")
    if "television" in category.lower() or "tv" in category.lower():
        return True
    
    return False


class SamsungRemoteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Samsung TV Remote."""
    
    VERSION = 2
    
    def __init__(self) -> None:
        """Initialize the config flow."""
        self._smartthings_entries: list[config_entries.ConfigEntry] = []
        self._selected_smartthings_entry: config_entries.ConfigEntry | None = None
        self._available_tvs: list[dict[str, str]] = []
    
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        # Get available SmartThings entries
        self._smartthings_entries = await _get_smartthings_entries(self.hass)
        
        if not self._smartthings_entries:
            return self.async_abort(reason="no_smartthings")
        
        # If only one SmartThings entry, skip selection
        if len(self._smartthings_entries) == 1:
            self._selected_smartthings_entry = self._smartthings_entries[0]
            return await self.async_step_select_tv()
        
        if user_input is not None:
            selected_entry_id = user_input.get("smartthings_entry")
            self._selected_smartthings_entry = next(
                (e for e in self._smartthings_entries if e.entry_id == selected_entry_id),
                None,
            )
            if self._selected_smartthings_entry:
                return await self.async_step_select_tv()
            errors["base"] = "invalid_entry"
        
        # Create entry selection schema
        entry_options = {
            entry.entry_id: entry.title or "SmartThings"
            for entry in self._smartthings_entries
        }
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("smartthings_entry"): vol.In(entry_options),
            }),
            errors=errors,
            description_placeholders={
                "count": str(len(self._smartthings_entries)),
            },
        )
    
    async def async_step_select_tv(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle TV selection step."""
        errors: dict[str, str] = {}
        
        if not self._selected_smartthings_entry:
            return self.async_abort(reason="no_smartthings")
        
        # Get available Samsung TVs
        self._available_tvs = await _get_samsung_tvs(
            self.hass, self._selected_smartthings_entry
        )
        
        if not self._available_tvs:
            return self.async_abort(reason="no_tvs_found")
        
        if user_input is not None:
            device_id = user_input.get("device_id")
            selected_tv = next(
                (tv for tv in self._available_tvs if tv["id"] == device_id),
                None,
            )
            
            if selected_tv:
                # Check if already configured
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=selected_tv["name"],
                    data={
                        CONF_DEVICE_ID: device_id,
                        CONF_DEVICE_NAME: selected_tv["name"],
                        CONF_SMARTTHINGS_ENTRY_ID: self._selected_smartthings_entry.entry_id,
                    },
                )
            errors["base"] = "invalid_device"
        
        # Create TV selection schema
        tv_options = {tv["id"]: tv["name"] for tv in self._available_tvs}
        
        return self.async_show_form(
            step_id="select_tv",
            data_schema=vol.Schema({
                vol.Required("device_id"): vol.In(tv_options),
            }),
            errors=errors,
            description_placeholders={
                "count": str(len(self._available_tvs)),
            },
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return SamsungRemoteOptionsFlow(config_entry)


class SamsungRemoteOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Samsung TV Remote."""
    
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
    
    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "scan_interval",
                    default=self.config_entry.options.get("scan_interval", 30),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
            }),
        )
