"""Remote entity for Samsung TV Remote integration."""
from __future__ import annotations

import logging
from typing import Any, Iterable

from homeassistant.components.remote import RemoteEntity, RemoteEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_NAME, SMARTTHINGS_COMMANDS, ACTIVITIES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Samsung TV Remote entity from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    bridge = data["bridge"]
    device_id = data["device_id"]
    
    async_add_entities([
        SamsungTVRemote(
            bridge=bridge,
            device_id=device_id,
            device_name=entry.data.get(CONF_DEVICE_NAME, "Samsung TV"),
            entry_id=entry.entry_id,
        )
    ])


class SamsungTVRemote(RemoteEntity):
    """Samsung TV Remote entity."""
    
    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_features = (
        RemoteEntityFeature.ACTIVITY
    )
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
        entry_id: str,
    ) -> None:
        """Initialize the remote entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._entry_id = entry_id
        self._attr_unique_id = f"{device_id}_remote"
        self._attr_is_on = False
        self._current_activity: str | None = None
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
    @property
    def is_on(self) -> bool:
        """Return true if the TV is on."""
        return self._attr_is_on
    
    @property
    def current_activity(self) -> str | None:
        """Return the current activity."""
        return self._current_activity
    
    @property
    def activity_list(self) -> list[str]:
        """Return the list of available activities."""
        return list(ACTIVITIES)
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the TV."""
        if await self._bridge.send_command("POWER_ON"):
            self._attr_is_on = True
            self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the TV."""
        if await self._bridge.send_command("POWER_OFF"):
            self._attr_is_on = False
            self.async_write_ha_state()
    
    async def async_send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        """Send commands to the TV."""
        num_repeats = kwargs.get("num_repeats", 1)
        delay_secs = kwargs.get("delay_secs", 0.4)
        
        for _ in range(num_repeats):
            for cmd in command:
                cmd_upper = cmd.upper()
                if cmd_upper in SMARTTHINGS_COMMANDS:
                    await self._bridge.send_command(cmd_upper)
                    if delay_secs > 0:
                        import asyncio
                        await asyncio.sleep(delay_secs)
                else:
                    _LOGGER.warning("Unknown command: %s", cmd)
    
    async def async_update(self) -> None:
        """Update the entity state."""
        self._attr_is_on = await self._bridge.get_power_state()
        self._attr_available = self._bridge.available
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        return {
            "supported_commands": list(SMARTTHINGS_COMMANDS.keys()),
            "device_id": self._device_id,
            "entry_id": self._entry_id,
        }
