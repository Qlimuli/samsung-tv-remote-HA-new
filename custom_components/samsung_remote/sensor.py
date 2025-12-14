"""Sensor entities for Samsung TV Remote integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
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
    """Set up Samsung TV Remote sensor entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    bridge = data["bridge"]
    device_id = data["device_id"]
    device_name = entry.data.get(CONF_DEVICE_NAME, "Samsung TV")
    
    entities = [
        SamsungTVActivitySensor(bridge, device_id, device_name),
        SamsungTVMediaTitleSensor(bridge, device_id, device_name),
        SamsungTVAppSensor(bridge, device_id, device_name),
    ]
    
    async_add_entities(entities)


class SamsungTVActivitySensor(SensorEntity):
    """Samsung TV current activity sensor entity."""
    
    _attr_has_entity_name = True
    _attr_name = "Activity"
    _attr_icon = "mdi:television-play"
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the activity sensor entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_activity_sensor"
        self._attr_native_value = "unknown"
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
    async def async_update(self) -> None:
        """Update the entity state."""
        activity = await self._bridge.get_current_activity()
        if activity:
            self._attr_native_value = activity


class SamsungTVMediaTitleSensor(SensorEntity):
    """Samsung TV media title sensor entity."""
    
    _attr_has_entity_name = True
    _attr_name = "Media Title"
    _attr_icon = "mdi:movie"
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the media title sensor entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_media_title_sensor"
        self._attr_native_value = None
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
    async def async_update(self) -> None:
        """Update the entity state."""
        title = await self._bridge.get_media_title()
        self._attr_native_value = title


class SamsungTVAppSensor(SensorEntity):
    """Samsung TV current app sensor entity."""
    
    _attr_has_entity_name = True
    _attr_name = "Current App"
    _attr_icon = "mdi:application"
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the app sensor entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_app_sensor"
        self._attr_native_value = None
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
    async def async_update(self) -> None:
        """Update the entity state."""
        app = await self._bridge.get_current_app()
        self._attr_native_value = app
