"""Select entities for Samsung TV Remote integration."""
from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_DEVICE_ID, CONF_DEVICE_NAME, HDMI_SOURCES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Samsung TV Remote select entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    bridge = data["bridge"]
    device_id = data["device_id"]
    device_name = entry.data.get(CONF_DEVICE_NAME, "Samsung TV")
    
    entities = [
        SamsungTVSourceSelect(bridge, device_id, device_name),
    ]
    
    async_add_entities(entities)


class SamsungTVSourceSelect(SelectEntity):
    """Samsung TV source select entity."""
    
    _attr_has_entity_name = True
    _attr_name = "Input Source"
    _attr_icon = "mdi:video-input-hdmi"
    _attr_options = HDMI_SOURCES
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the source select entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_source_select"
        self._attr_current_option = None
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
    async def async_select_option(self, option: str) -> None:
        """Select an input source."""
        if await self._bridge.send_command(option):
            self._attr_current_option = option
            self.async_write_ha_state()
    
    async def async_update(self) -> None:
        """Update the entity state."""
        source = await self._bridge.get_input_source()
        if source and source in HDMI_SOURCES:
            self._attr_current_option = source
