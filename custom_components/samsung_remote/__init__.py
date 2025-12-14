"""Samsung TV Remote Integration for Home Assistant.

This integration uses the existing SmartThings integration for authentication,
eliminating the need for separate token management.
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_DEVICE_ID, CONF_SMARTTHINGS_ENTRY_ID
from .smartthings_bridge import SmartThingsBridge

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.REMOTE,
    Platform.BUTTON,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Samsung Remote from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    smartthings_entry_id = entry.data.get(CONF_SMARTTHINGS_ENTRY_ID)
    device_id = entry.data.get(CONF_DEVICE_ID)
    
    if not smartthings_entry_id or not device_id:
        _LOGGER.error("Missing SmartThings entry ID or device ID")
        return False
    
    # Get the SmartThings integration entry
    smartthings_entry = hass.config_entries.async_get_entry(smartthings_entry_id)
    if not smartthings_entry:
        _LOGGER.error("SmartThings integration not found: %s", smartthings_entry_id)
        raise ConfigEntryNotReady("SmartThings integration not found")
    
    # Create the bridge to SmartThings
    try:
        bridge = SmartThingsBridge(hass, smartthings_entry, device_id)
        await bridge.async_initialize()
    except Exception as err:
        _LOGGER.error("Failed to initialize SmartThings bridge: %s", err)
        raise ConfigEntryNotReady(f"Failed to connect: {err}") from err
    
    hass.data[DOMAIN][entry.entry_id] = {
        "bridge": bridge,
        "device_id": device_id,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services
    await async_register_services(hass)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_register_services(hass: HomeAssistant) -> None:
    """Register custom services."""
    
    async def handle_send_key(call) -> None:
        """Handle the send_key service call."""
        entry_id = call.data.get("entry_id")
        key = call.data.get("key")
        
        if entry_id and entry_id in hass.data[DOMAIN]:
            bridge = hass.data[DOMAIN][entry_id]["bridge"]
            await bridge.send_command(key)
    
    if not hass.services.has_service(DOMAIN, "send_key"):
        hass.services.async_register(DOMAIN, "send_key", handle_send_key)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)
    
    if config_entry.version == 1:
        # Migration from v1 to v2 - now using SmartThings integration
        _LOGGER.info("Migration from v1 to v2 requires reconfiguration")
        return False
    
    return True
