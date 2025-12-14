"""Bridge to SmartThings integration for authentication and API calls.

This module directly accesses the SmartThings OAuth tokens stored in the
config entry, exactly like the native SmartThings integration does.
"""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import SMARTTHINGS_API_BASE, SMARTTHINGS_COMMANDS

_LOGGER = logging.getLogger(__name__)


class SmartThingsBridge:
    """Bridge class to interact with SmartThings using existing integration auth."""
    
    def __init__(
        self,
        hass: HomeAssistant,
        smartthings_entry: ConfigEntry,
        device_id: str,
    ) -> None:
        """Initialize the SmartThings bridge."""
        self.hass = hass
        self.smartthings_entry = smartthings_entry
        self.device_id = device_id
        self._device_info: dict[str, Any] = {}
        self._available = False
        self._cached_status: dict[str, Any] = {}
    
    @property
    def available(self) -> bool:
        """Return if the device is available."""
        return self._available
    
    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return self._device_info
    
    def _get_access_token(self) -> str | None:
        """Get access token from SmartThings integration.
        
        The SmartThings integration stores the OAuth token in different places
        depending on the version. We try multiple approaches.
        """
        entry_data = self.smartthings_entry.data
        
        # Check for token structure from OAuth flow
        if "token" in entry_data:
            token_data = entry_data["token"]
            if isinstance(token_data, dict):
                if "access_token" in token_data:
                    _LOGGER.debug("Found access_token in token dict")
                    return token_data["access_token"]
            elif isinstance(token_data, str):
                _LOGGER.debug("Found token as string")
                return token_data
        
        # Direct access_token in data
        if "access_token" in entry_data:
            _LOGGER.debug("Found direct access_token in entry data")
            return entry_data["access_token"]
        
        if hasattr(self.smartthings_entry, "runtime_data"):
            runtime_data = self.smartthings_entry.runtime_data
            
            # SmartThings 2025 uses SmartThingsData dataclass
            if hasattr(runtime_data, "client"):
                client = runtime_data.client
                # pysmartthings client stores token
                if hasattr(client, "_token"):
                    _LOGGER.debug("Found token in runtime_data.client._token")
                    return client._token
                if hasattr(client, "_session"):
                    session = client._session
                    if hasattr(session, "_token"):
                        return session._token
            
            # Check if runtime_data itself has token info
            if hasattr(runtime_data, "token"):
                return runtime_data.token
        
        smartthings_data = self.hass.data.get("smartthings", {})
        
        # Try entry_id based lookup
        if self.smartthings_entry.entry_id in smartthings_data:
            st_entry_data = smartthings_data[self.smartthings_entry.entry_id]
            
            if hasattr(st_entry_data, "client"):
                client = st_entry_data.client
                if hasattr(client, "_token"):
                    return client._token
            
            if isinstance(st_entry_data, dict):
                if "client" in st_entry_data:
                    client = st_entry_data["client"]
                    if hasattr(client, "_token"):
                        return client._token
        
        for key, data in smartthings_data.items():
            if hasattr(data, "client"):
                client = data.client
                if hasattr(client, "_token"):
                    _LOGGER.debug("Found token via iteration in smartthings data")
                    return client._token
        
        _LOGGER.warning("Could not retrieve access token from SmartThings integration")
        return None
    
    async def async_initialize(self) -> None:
        """Initialize the bridge and fetch device info."""
        token = self._get_access_token()
        if not token:
            raise ValueError("No valid SmartThings token available")
        
        # Fetch device information
        self._device_info = await self._fetch_device_info(token)
        self._available = True
        _LOGGER.info("SmartThings bridge initialized for device: %s", self.device_id)
    
    async def _fetch_device_info(self, token: str) -> dict[str, Any]:
        """Fetch device information from SmartThings API."""
        url = f"{SMARTTHINGS_API_BASE}/devices/{self.device_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    raise ValueError("SmartThings token expired or invalid")
                else:
                    error_text = await response.text()
                    raise ValueError(f"Failed to fetch device info: {response.status} - {error_text}")
    
    async def send_command(self, command: str) -> bool:
        """Send a command to the Samsung TV."""
        token = self._get_access_token()
        if not token:
            _LOGGER.error("No valid SmartThings token available")
            return False
        
        command_upper = command.upper()
        
        if command_upper not in SMARTTHINGS_COMMANDS:
            _LOGGER.warning("Unknown command: %s", command)
            return False
        
        cmd_config = SMARTTHINGS_COMMANDS[command_upper]
        
        url = f"{SMARTTHINGS_API_BASE}/devices/{self.device_id}/commands"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "commands": [
                {
                    "component": cmd_config["component"],
                    "capability": cmd_config["capability"],
                    "command": cmd_config["command"],
                    "arguments": cmd_config["args"],
                }
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        _LOGGER.debug("Command %s sent successfully", command)
                        return True
                    else:
                        error_text = await response.text()
                        _LOGGER.error(
                            "Failed to send command %s: %s - %s",
                            command,
                            response.status,
                            error_text,
                        )
                        return False
        except Exception as err:
            _LOGGER.error("Error sending command %s: %s", command, err)
            return False
    
    async def get_device_status(self) -> dict[str, Any]:
        """Get the current status of the device."""
        token = self._get_access_token()
        if not token:
            return {}
        
        url = f"{SMARTTHINGS_API_BASE}/devices/{self.device_id}/status"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        self._cached_status = await response.json()
                        return self._cached_status
                    else:
                        _LOGGER.warning("Failed to get device status: %s", response.status)
                        return self._cached_status
        except Exception as err:
            _LOGGER.error("Error getting device status: %s", err)
            return self._cached_status
    
    async def get_power_state(self) -> bool:
        """Get the power state of the TV."""
        status = await self.get_device_status()
        try:
            switch_status = status.get("components", {}).get("main", {}).get("switch", {})
            return switch_status.get("switch", {}).get("value") == "on"
        except (KeyError, TypeError):
            return False
    
    async def get_mute_state(self) -> bool:
        """Get the mute state of the TV."""
        status = await self.get_device_status()
        try:
            mute_status = status.get("components", {}).get("main", {}).get("audioMute", {})
            return mute_status.get("mute", {}).get("value") == "muted"
        except (KeyError, TypeError):
            return False
    
    async def get_volume(self) -> int | None:
        """Get the current volume level."""
        status = await self.get_device_status()
        try:
            volume_status = status.get("components", {}).get("main", {}).get("audioVolume", {})
            return volume_status.get("volume", {}).get("value")
        except (KeyError, TypeError):
            return None
    
    async def set_volume(self, volume: int) -> bool:
        """Set the volume level."""
        token = self._get_access_token()
        if not token:
            return False
        
        url = f"{SMARTTHINGS_API_BASE}/devices/{self.device_id}/commands"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "commands": [
                {
                    "component": "main",
                    "capability": "audioVolume",
                    "command": "setVolume",
                    "arguments": [volume],
                }
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    return response.status == 200
        except Exception as err:
            _LOGGER.error("Error setting volume: %s", err)
            return False
    
    async def get_channel(self) -> int | None:
        """Get the current channel number."""
        status = await self.get_device_status()
        try:
            channel_status = status.get("components", {}).get("main", {}).get("tvChannel", {})
            channel = channel_status.get("tvChannel", {}).get("value")
            if channel:
                try:
                    return int(channel)
                except (ValueError, TypeError):
                    return None
            return None
        except (KeyError, TypeError):
            return None
    
    async def set_channel(self, channel: int) -> bool:
        """Set the TV channel."""
        token = self._get_access_token()
        if not token:
            return False
        
        url = f"{SMARTTHINGS_API_BASE}/devices/{self.device_id}/commands"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "commands": [
                {
                    "component": "main",
                    "capability": "tvChannel",
                    "command": "setTvChannel",
                    "arguments": [str(channel)],
                }
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    return response.status == 200
        except Exception as err:
            _LOGGER.error("Error setting channel: %s", err)
            return False
    
    async def get_input_source(self) -> str | None:
        """Get the current input source."""
        status = await self.get_device_status()
        try:
            input_status = status.get("components", {}).get("main", {}).get("mediaInputSource", {})
            return input_status.get("inputSource", {}).get("value")
        except (KeyError, TypeError):
            return None
    
    async def get_current_activity(self) -> str | None:
        """Get the current activity (playing, paused, etc.)."""
        status = await self.get_device_status()
        try:
            playback_status = status.get("components", {}).get("main", {}).get("mediaPlayback", {})
            return playback_status.get("playbackStatus", {}).get("value")
        except (KeyError, TypeError):
            return None
    
    async def get_media_title(self) -> str | None:
        """Get the current media title."""
        status = await self.get_device_status()
        try:
            # Try mediaTrackData first
            track_data = status.get("components", {}).get("main", {}).get("mediaTrackData", {})
            title = track_data.get("mediaTrackData", {}).get("value", {})
            if isinstance(title, dict):
                return title.get("title")
            return None
        except (KeyError, TypeError):
            return None
    
    async def get_current_app(self) -> str | None:
        """Get the current running app."""
        status = await self.get_device_status()
        try:
            # Try different capability names that Samsung TVs might use
            for cap_name in ["samsungvd.launchApp", "custom.launchApp", "mediaInputSource"]:
                app_status = status.get("components", {}).get("main", {}).get(cap_name, {})
                if app_status:
                    for key in ["appName", "currentApp", "inputSource"]:
                        app = app_status.get(key, {}).get("value")
                        if app:
                            return app
            return None
        except (KeyError, TypeError):
            return None


async def get_smartthings_token(hass: HomeAssistant, entry: ConfigEntry) -> str | None:
    """Get SmartThings access token from config entry."""
    entry_data = entry.data
    
    # OAuth token in data.token
    if "token" in entry_data:
        token_data = entry_data["token"]
        if isinstance(token_data, dict) and "access_token" in token_data:
            return token_data["access_token"]
        elif isinstance(token_data, str):
            return token_data
    
    # Direct access_token
    if "access_token" in entry_data:
        return entry_data["access_token"]
    
    # Check runtime_data
    if hasattr(entry, "runtime_data"):
        runtime_data = entry.runtime_data
        if hasattr(runtime_data, "client"):
            client = runtime_data.client
            if hasattr(client, "_token"):
                return client._token
    
    # Check hass.data
    smartthings_data = hass.data.get("smartthings", {})
    if entry.entry_id in smartthings_data:
        st_data = smartthings_data[entry.entry_id]
        if hasattr(st_data, "client") and hasattr(st_data.client, "_token"):
            return st_data.client._token
    
    return None


async def fetch_all_devices(token: str) -> list[dict[str, Any]]:
    """Fetch all devices from SmartThings API."""
    url = f"{SMARTTHINGS_API_BASE}/devices"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    devices = []
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                devices = data.get("items", [])
            else:
                _LOGGER.error("Failed to fetch devices: %s", response.status)
    
    return devices


def is_samsung_tv(device: dict[str, Any]) -> bool:
    """Check if a device is a Samsung TV."""
    # Check device type name
    device_type = device.get("deviceTypeName", "").lower()
    name = device.get("name", "").lower()
    label = device.get("label", "").lower()
    
    # Check manufacturer
    manufacturer = device.get("manufacturerName", "").lower()
    
    # Check OCF device type
    ocf = device.get("ocf", {})
    ocf_type = ocf.get("ocfDeviceType", "").lower()
    
    # Check categories
    categories = device.get("components", [{}])[0].get("categories", [])
    category_names = [c.get("name", "").lower() for c in categories if isinstance(c, dict)]
    
    # Check capabilities
    capabilities = []
    for component in device.get("components", []):
        for cap in component.get("capabilities", []):
            cap_id = cap.get("id", "") if isinstance(cap, dict) else str(cap)
            capabilities.append(cap_id.lower())
    
    # Samsung TV indicators
    tv_indicators = [
        "samsung" in manufacturer and "tv" in device_type,
        "samsung" in manufacturer and "tv" in name,
        "samsung" in manufacturer and "tv" in label,
        "television" in category_names,
        "tv" in category_names,
        "oic.d.tv" in ocf_type,
        "samsungvd.remotecontrol" in capabilities,
        "samsungvd.mediaInputsource" in capabilities,
        any("samsungvd" in cap and "tv" in cap for cap in capabilities),
    ]
    
    # Also check for general TV capabilities with Samsung manufacturer
    general_tv_caps = [
        "tvchannel" in capabilities,
        "mediaplayback" in capabilities and "switch" in capabilities,
    ]
    
    is_tv = any(tv_indicators) or (
        "samsung" in manufacturer and any(general_tv_caps)
    )
    
    _LOGGER.debug(
        "Device check - Name: %s, Manufacturer: %s, Type: %s, OCF: %s, Categories: %s, Is TV: %s",
        label or name,
        manufacturer,
        device_type,
        ocf_type,
        category_names,
        is_tv
    )
    
    return is_tv


async def get_samsung_tvs_from_api(
    hass: HomeAssistant, 
    smartthings_entry: ConfigEntry
) -> list[dict[str, str]]:
    """Get Samsung TVs directly from SmartThings API."""
    token = await get_smartthings_token(hass, smartthings_entry)
    
    if not token:
        _LOGGER.error("No SmartThings token available")
        return []
    
    devices = await fetch_all_devices(token)
    tvs = []
    
    for device in devices:
        if is_samsung_tv(device):
            tvs.append({
                "id": device.get("deviceId"),
                "name": device.get("label") or device.get("name") or "Samsung TV",
                "manufacturer": device.get("manufacturerName", "Samsung"),
                "model": device.get("deviceTypeName", "TV"),
            })
    
    _LOGGER.info("Found %d Samsung TV(s) in SmartThings account", len(tvs))
    return tvs
