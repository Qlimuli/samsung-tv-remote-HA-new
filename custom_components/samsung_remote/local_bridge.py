"""Local WebSocket bridge for Samsung Tizen TVs.

Uses the samsungtvws library (WebSocket on port 8001/8002) for fully local
control – no SmartThings cloud required.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import LOCAL_KEY_MAP

_LOGGER = logging.getLogger(__name__)

# Lazy import so the cloud-only install still works if samsungtvws is missing
try:
    from samsungtvws.async_remote import SamsungTVWSAsyncRemote
    from samsungtvws.remote import SendRemoteKey
    from samsungtvws.async_rest import SamsungTVAsyncRest
    import wakeonlan

    HAS_SAMSUNGTVWS = True
except ImportError:  # pragma: no cover
    HAS_SAMSUNGTVWS = False
    SamsungTVWSAsyncRemote = None  # type: ignore
    SendRemoteKey = None  # type: ignore
    SamsungTVAsyncRest = None  # type: ignore
    wakeonlan = None  # type: ignore


class LocalBridge:
    """Local control of a Samsung Tizen TV via WebSocket + REST."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        *,
        token: str | None = None,
        port: int = 8002,
        name: str = "Home Assistant",
        mac: str | None = None,
        timeout: float = 5.0,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        if not HAS_SAMSUNGTVWS:
            raise RuntimeError(
                "samsungtvws is not installed. Add 'samsungtvws[async]>=2.6.0' "
                "and 'wakeonlan>=3.0.0' to the integration requirements."
            )

        self.hass = hass
        self.host = host
        self.port = port
        self.token = token
        self.name = name
        self.mac = mac
        self.timeout = timeout
        # Prefer HA's shared session; fall back only when none is provided
        self._session = session or async_get_clientsession(hass)

        self._remote: SamsungTVWSAsyncRemote | None = None
        self._rest: SamsungTVAsyncRest | None = None
        self._available = False
        self._device_info: dict[str, Any] = {}
        self._power_on = False
        self._mute = False
        self._volume: int | None = None
        self._app_name: str | None = None
        self._lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # Properties (same surface as SmartThingsBridge)
    # ------------------------------------------------------------------

    @property
    def available(self) -> bool:
        return self._available

    @property
    def device_info(self) -> dict[str, Any]:
        return self._device_info

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def async_initialize(self) -> None:
        """Connect and fetch basic device info."""
        try:
            await self._ensure_remote()
        except Exception as err:
            _LOGGER.debug("WebSocket connect during init: %s", err)

        try:
            info = await self._rest_device_info()
            if info:
                self._device_info = info
                self._power_on = True
            self._available = True
            _LOGGER.info("Local bridge connected to %s:%s", self.host, self.port)
        except Exception as err:
            _LOGGER.warning("Local bridge init partial failure on %s: %s", self.host, err)
            # Still mark available if we at least got a token / WS connection
            if self.token or self._remote is not None:
                self._available = True

    async def async_close(self) -> None:
        """Close WebSocket connection."""
        if self._remote is not None:
            try:
                await self._remote.close()
            except Exception:  # noqa: BLE001
                pass
            self._remote = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_rest(self) -> SamsungTVAsyncRest:
        """Lazy-create REST client with required session argument."""
        if self._rest is None:
            self._rest = SamsungTVAsyncRest(
                host=self.host,
                session=self._session,
                port=8001,  # REST is on 8001 on virtually all models
                timeout=self.timeout,
            )
        return self._rest

    async def _ensure_remote(self) -> SamsungTVWSAsyncRemote:
        async with self._lock:
            if self._remote is not None:
                return self._remote

            remote = SamsungTVWSAsyncRemote(
                host=self.host,
                token=self.token,
                port=self.port,
                timeout=self.timeout,
                name=self.name,
            )
            try:
                await remote.start_listening()
            except Exception as err:
                _LOGGER.debug("start_listening failed (TV may be off / pairing): %s", err)

            # Capture token if the TV issued a new one
            new_token = getattr(remote, "token", None)
            if new_token and new_token != self.token:
                self.token = new_token
                _LOGGER.info("Received new token from TV %s", self.host)

            self._remote = remote
            return remote

    async def _rest_device_info(self) -> dict[str, Any]:
        try:
            rest = self._get_rest()
            return await rest.rest_device_info()
        except Exception as err:
            _LOGGER.debug("REST device info failed: %s", err)
            return {}

    def _map_key(self, command: str) -> str | None:
        """Map high-level command to KEY_*."""
        return LOCAL_KEY_MAP.get(command.upper())

    # ------------------------------------------------------------------
    # Public API – same method names as SmartThingsBridge
    # ------------------------------------------------------------------

    async def send_command(self, command: str) -> bool:
        """Send a high-level command (UP, HOME, POWER_OFF, …)."""
        key = self._map_key(command)
        if not key:
            _LOGGER.warning("Unknown local command: %s", command)
            return False

        cmd = command.upper()

        # Special handling for power-on when TV is fully off
        if cmd in ("POWER_ON", "POWER") and not self._power_on:
            if self.mac and wakeonlan is not None:
                try:
                    await self.hass.async_add_executor_job(
                        wakeonlan.send_magic_packet, self.mac
                    )
                    _LOGGER.debug("WOL packet sent to %s", self.mac)
                    await asyncio.sleep(2)
                except Exception as err:
                    _LOGGER.debug("WOL failed: %s", err)

        try:
            remote = await self._ensure_remote()
            await remote.send_command(SendRemoteKey.click(key))
            self._available = True
            if cmd in ("POWER_OFF", "POWER"):
                self._power_on = False
            elif cmd == "POWER_ON":
                self._power_on = True
            elif cmd == "MUTE":
                self._mute = True
            elif cmd == "UNMUTE":
                self._mute = False
            return True
        except Exception as err:
            _LOGGER.error("Failed to send %s (%s): %s", command, key, err)
            self._available = False
            # Reset remote so next call reconnects
            await self.async_close()
            return False

    async def get_device_status(self) -> dict[str, Any]:
        """Best-effort status (local API is limited compared to SmartThings)."""
        return await self._rest_device_info() or {}

    async def get_power_state(self) -> bool:
        """Return True if TV appears to be on."""
        try:
            info = await self._rest_device_info()
            if info:
                self._power_on = True
                self._available = True
                return True
        except Exception:
            pass

        try:
            remote = await self._ensure_remote()
            self._available = remote is not None
            return self._power_on
        except Exception:
            self._available = False
            self._power_on = False
            return False

    async def get_mute_state(self) -> bool:
        """Local API does not expose mute state reliably → last known."""
        return self._mute

    async def get_volume(self) -> int | None:
        """Volume level is not reliably readable on pure local WS."""
        return self._volume

    async def set_volume(self, volume: int) -> bool:
        """Absolute volume is not supported on pure local WS."""
        _LOGGER.debug(
            "set_volume(%s) not supported natively on local WS – use VOLUME_UP/DOWN",
            volume,
        )
        return False

    async def get_channel(self) -> int | None:
        return None

    async def set_channel(self, channel: int) -> bool:
        """Send channel digits one by one."""
        try:
            for digit in str(channel):
                if not await self.send_command(digit):
                    return False
                await asyncio.sleep(0.3)
            return True
        except Exception as err:
            _LOGGER.error("set_channel failed: %s", err)
            return False

    async def get_input_source(self) -> str | None:
        return None

    async def get_current_activity(self) -> str | None:
        return None

    async def get_media_title(self) -> str | None:
        return None

    async def get_current_app(self) -> str | None:
        return self._app_name
