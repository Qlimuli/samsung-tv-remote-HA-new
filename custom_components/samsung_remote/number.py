"""Number entities for Samsung TV Remote integration."""
from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity, NumberMode
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
    """Set up Samsung TV Remote number entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    bridge = data["bridge"]
    device_id = data["device_id"]
    device_name = entry.data.get(CONF_DEVICE_NAME, "Samsung TV")
    
    entities = [
        SamsungTVVolumeNumber(bridge, device_id, device_name),
        SamsungTVChannelNumber(bridge, device_id, device_name),
    ]
    
    async_add_entities(entities)


class SamsungTVVolumeNumber(NumberEntity):
    """Samsung TV volume number entity."""
    
    _attr_has_entity_name = True
    _attr_name = "Volume"
    _attr_icon = "mdi:volume-high"
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the volume number entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_volume_number"
        self._attr_native_value = 0
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
    async def async_set_native_value(self, value: float) -> None:
        """Set the volume level."""
        if await self._bridge.set_volume(int(value)):
            self._attr_native_value = value
            self.async_write_ha_state()
    
    async def async_update(self) -> None:
        """Update the entity state."""
        volume = await self._bridge.get_volume()
        if volume is not None:
            self._attr_native_value = volume


class SamsungTVChannelNumber(NumberEntity):
    """Samsung TV channel number entity."""
    
    _attr_has_entity_name = True
    _attr_name = "Channel"
    _attr_icon = "mdi:television-classic"
    _attr_native_min_value = 1
    _attr_native_max_value = 9999
    _attr_native_step = 1
    _attr_mode = NumberMode.BOX
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the channel number entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_channel_number"
        self._attr_native_value = 1
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
    async def async_set_native_value(self, value: float) -> None:
        """Set the channel."""
        if await self._bridge.set_channel(int(value)):
            self._attr_native_value = value
            self.async_write_ha_state()
    
    async def async_update(self) -> None:
        """Update the entity state."""
        channel = await self._bridge.get_channel()
        if channel is not None:
            self._attr_native_value = channel
