"""Samsung TV Remote Integration for Home Assistant.

Supports two connection modes:
- Cloud: uses the existing SmartThings integration for authentication
- Local: direct WebSocket control on the LAN (no cloud, no paid API)
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    DOMAIN,
    CONF_DEVICE_ID,
    CONF_SMARTTHINGS_ENTRY_ID,
    CONF_CONNECTION_MODE,
    CONF_HOST,
    CONF_PORT,
    CONF_TOKEN,
    CONF_MAC,
    CONF_DEVICE_NAME,
    MODE_CLOUD,
    MODE_LOCAL,
)

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

    # Prefer explicit mode; fall back to heuristic so a local entry that only
    # has "host" is never treated as cloud (and never touches SmartThings).
    mode = entry.data.get(CONF_CONNECTION_MODE)
    if mode is None:
        if entry.data.get(CONF_HOST):
            mode = MODE_LOCAL
        else:
            mode = MODE_CLOUD

    if mode == MODE_LOCAL:
        bridge = await _setup_local(hass, entry)
    else:
        bridge = await _setup_cloud(hass, entry)

    device_id = entry.data.get(CONF_DEVICE_ID) or entry.data.get(CONF_HOST, entry.entry_id)

    hass.data[DOMAIN][entry.entry_id] = {
        "bridge": bridge,
        "device_id": device_id,
        "mode": mode,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await async_register_services(hass)

    return True


async def _setup_cloud(hass: HomeAssistant, entry: ConfigEntry):
    """Create SmartThings cloud bridge."""
    from .smartthings_bridge import SmartThingsBridge

    smartthings_entry_id = entry.data.get(CONF_SMARTTHINGS_ENTRY_ID)
    device_id = entry.data.get(CONF_DEVICE_ID)

    if not smartthings_entry_id or not device_id:
        _LOGGER.error("Missing SmartThings entry ID or device ID")
        raise ConfigEntryNotReady("Missing SmartThings configuration")

    smartthings_entry = hass.config_entries.async_get_entry(smartthings_entry_id)
    if not smartthings_entry:
        _LOGGER.error("SmartThings integration not found: %s", smartthings_entry_id)
        raise ConfigEntryNotReady("SmartThings integration not found")

    try:
        bridge = SmartThingsBridge(hass, smartthings_entry, device_id)
        await bridge.async_initialize()
    except Exception as err:
        _LOGGER.error("Failed to initialize SmartThings bridge: %s", err)
        raise ConfigEntryNotReady(f"Failed to connect: {err}") from err

    return bridge


async def _setup_local(hass: HomeAssistant, entry: ConfigEntry):
    """Create local WebSocket bridge."""
    from .local_bridge import LocalBridge

    host = entry.data.get(CONF_HOST)
    if not host:
        raise ConfigEntryNotReady("Missing host for local mode")

    try:
        bridge = LocalBridge(
            hass,
            host=host,
            token=entry.data.get(CONF_TOKEN),
            port=entry.data.get(CONF_PORT, 8002),
            name=entry.data.get(CONF_DEVICE_NAME, "Home Assistant"),
            mac=entry.data.get(CONF_MAC),
        )
        await bridge.async_initialize()
    except Exception as err:
        _LOGGER.error("Failed to initialize local bridge: %s", err)
        raise ConfigEntryNotReady(f"Failed to connect locally: {err}") from err

    # Persist token if the TV issued a new one during pairing
    if bridge.token and bridge.token != entry.data.get(CONF_TOKEN):
        new_data = {**entry.data, CONF_TOKEN: bridge.token}
        hass.config_entries.async_update_entry(entry, data=new_data)
        _LOGGER.info("Stored new pairing token for %s", host)

    return bridge


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        data = hass.data[DOMAIN].pop(entry.entry_id, None)
        if data and data.get("mode") == MODE_LOCAL:
            bridge = data.get("bridge")
            if bridge and hasattr(bridge, "async_close"):
                await bridge.async_close()
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
        _LOGGER.info("Migration from v1 to v2 requires reconfiguration")
        return False

    # v2 → v3: add connection_mode default for existing cloud entries
    if config_entry.version == 2:
        data = {**config_entry.data}
        if CONF_CONNECTION_MODE not in data:
            data[CONF_CONNECTION_MODE] = MODE_CLOUD
        hass.config_entries.async_update_entry(config_entry, data=data, version=3)
        return True

    return True
