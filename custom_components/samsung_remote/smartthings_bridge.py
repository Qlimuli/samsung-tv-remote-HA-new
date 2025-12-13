"""Bridge to SmartThings integration for authentication and API calls."""
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
    
    @property
    def available(self) -> bool:
        """Return if the device is available."""
        return self._available
    
    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return self._device_info
    
    def _get_access_token(self) -> str | None:
        """Get access token from SmartThings integration."""
        # Access the SmartThings integration data
        smartthings_data = self.hass.data.get("smartthings", {})
        
        # Try to get token from the integration's runtime data
        if hasattr(self.smartthings_entry, "runtime_data"):
            runtime_data = self.smartthings_entry.runtime_data
            if hasattr(runtime_data, "client"):
                client = runtime_data.client
                if hasattr(client, "_token"):
                    return client._token
                if hasattr(client, "token"):
                    return client.token
        
        # Fallback: Try to get from entry data
        entry_data = self.smartthings_entry.data
        if "token" in entry_data:
            return entry_data["token"]
        if "access_token" in entry_data:
            return entry_data["access_token"]
        
        # Try from smartthings domain data
        for entry_id, data in smartthings_data.items():
            if isinstance(data, dict) and "broker" in data:
                broker = data["broker"]
                if hasattr(broker, "_token"):
                    return broker._token
            # Check for SmartThings client
            if hasattr(data, "client"):
                client = data.client
                if hasattr(client, "_token"):
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
                        return await response.json()
                    else:
                        _LOGGER.warning("Failed to get device status: %s", response.status)
                        return {}
        except Exception as err:
            _LOGGER.error("Error getting device status: %s", err)
            return {}
    
    async def get_power_state(self) -> bool:
        """Get the power state of the TV."""
        status = await self.get_device_status()
        try:
            switch_status = status.get("components", {}).get("main", {}).get("switch", {})
            return switch_status.get("switch", {}).get("value") == "on"
        except (KeyError, TypeError):
            return False
