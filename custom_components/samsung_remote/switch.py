"""Switch entities for Samsung TV Remote integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_NAME

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Samsung TV Remote switch entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    bridge = data["bridge"]
    device_id = data["device_id"]
    device_name = entry.data.get(CONF_DEVICE_NAME, "Samsung TV")
    
    entities = [
        SamsungTVPowerSwitch(bridge, device_id, device_name),
        SamsungTVMuteSwitch(bridge, device_id, device_name),
    ]
    
    async_add_entities(entities)


class SamsungTVPowerSwitch(SwitchEntity):
    """Samsung TV power switch entity."""
    
    _attr_has_entity_name = True
    _attr_name = "Power"
    _attr_icon = "mdi:power"
    _attr_device_class = SwitchDeviceClass.SWITCH
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the power switch entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_power_switch"
        self._attr_is_on = False
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
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
    
    async def async_update(self) -> None:
        """Update the entity state."""
        self._attr_is_on = await self._bridge.get_power_state()


class SamsungTVMuteSwitch(SwitchEntity):
    """Samsung TV mute switch entity."""
    
    _attr_has_entity_name = True
    _attr_name = "Mute"
    _attr_icon = "mdi:volume-mute"
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the mute switch entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_mute_switch"
        self._attr_is_on = False
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Mute the TV."""
        if await self._bridge.send_command("MUTE"):
            self._attr_is_on = True
            self.async_write_ha_state()
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Unmute the TV."""
        if await self._bridge.send_command("UNMUTE"):
            self._attr_is_on = False
            self.async_write_ha_state()
    
    async def async_update(self) -> None:
        """Update the entity state."""
        self._attr_is_on = await self._bridge.get_mute_state()
