"""Config flow for Samsung TV Remote integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_NAME, CONF_SMARTTHINGS_ENTRY_ID
from .smartthings_bridge import get_samsung_tvs_from_api, get_smartthings_token

_LOGGER = logging.getLogger(__name__)


async def _get_smartthings_entries(hass: HomeAssistant) -> list[config_entries.ConfigEntry]:
    """Get all SmartThings config entries."""
    entries = []
    
    for domain in ["smartthings", "smartthings2"]:
        for entry in hass.config_entries.async_entries(domain):
            if entry.state == config_entries.ConfigEntryState.LOADED:
                entries.append(entry)
    
    return entries


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
            
            token = await get_smartthings_token(self.hass, self._selected_smartthings_entry)
            if not token:
                return self.async_abort(reason="no_token")
            
            return await self.async_step_select_tv()
        
        if user_input is not None:
            selected_entry_id = user_input.get("smartthings_entry")
            self._selected_smartthings_entry = next(
                (e for e in self._smartthings_entries if e.entry_id == selected_entry_id),
                None,
            )
            if self._selected_smartthings_entry:
                token = await get_smartthings_token(self.hass, self._selected_smartthings_entry)
                if not token:
                    errors["base"] = "no_token"
                else:
                    return await self.async_step_select_tv()
            else:
                errors["base"] = "invalid_entry"
        
        # Create entry selection schema
        entry_options = {
            entry.entry_id: entry.title or f"SmartThings ({entry.domain})"
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
        
        if not self._available_tvs:
            self._available_tvs = await get_samsung_tvs_from_api(
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
