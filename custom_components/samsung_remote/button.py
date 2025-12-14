"""Button entities for Samsung TV Remote integration."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    ALL_BUTTON_COMMANDS,
    NAVIGATION_COMMANDS,
    PLAYBACK_COMMANDS,
    CHANNEL_COMMANDS,
    NUMBER_COMMANDS,
    COLOR_COMMANDS,
    SPECIAL_COMMANDS,
    VOLUME_COMMANDS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Samsung TV Remote button entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    bridge = data["bridge"]
    device_id = data["device_id"]
    device_name = entry.data.get(CONF_DEVICE_NAME, "Samsung TV")
    
    entities = []
    
    # Create button entities for each command
    for cmd, cmd_info in ALL_BUTTON_COMMANDS.items():
        # Determine category for entity_id prefix
        if cmd in NAVIGATION_COMMANDS:
            category = "nav"
        elif cmd in PLAYBACK_COMMANDS:
            category = "playback"
        elif cmd in CHANNEL_COMMANDS:
            category = "channel"
        elif cmd in NUMBER_COMMANDS:
            category = "num"
        elif cmd in COLOR_COMMANDS:
            category = "color"
        elif cmd in SPECIAL_COMMANDS:
            category = "special"
        elif cmd in VOLUME_COMMANDS:
            category = "volume"
        else:
            category = "btn"
        
        entities.append(
            SamsungTVButton(
                bridge=bridge,
                device_id=device_id,
                device_name=device_name,
                command=cmd,
                command_name=cmd_info["name"],
                icon=cmd_info["icon"],
                category=category,
            )
        )
    
    async_add_entities(entities)


class SamsungTVButton(ButtonEntity):
    """Samsung TV button entity for remote commands."""
    
    _attr_has_entity_name = True
    
    def __init__(
        self,
        bridge,
        device_id: str,
        device_name: str,
        command: str,
        command_name: str,
        icon: str,
        category: str,
    ) -> None:
        """Initialize the button entity."""
        self._bridge = bridge
        self._device_id = device_id
        self._device_name = device_name
        self._command = command
        self._attr_name = command_name
        self._attr_icon = icon
        self._attr_unique_id = f"{device_id}_{category}_{command.lower()}"
        self._category = category
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung",
            model="Smart TV",
        )
    
    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.debug("Button pressed: %s", self._command)
        await self._bridge.send_command(self._command)
