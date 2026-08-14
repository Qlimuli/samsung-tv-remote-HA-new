"""Config flow for Samsung TV Remote integration.

Supports two modes:
- Cloud (SmartThings) – existing behaviour
- Local (WebSocket) – fully offline control via LAN
"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    CONF_SMARTTHINGS_ENTRY_ID,
    CONF_CONNECTION_MODE,
    CONF_HOST,
    CONF_PORT,
    CONF_TOKEN,
    CONF_MAC,
    MODE_CLOUD,
    MODE_LOCAL,
)

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 8002


async def _get_smartthings_entries(hass: HomeAssistant) -> list[config_entries.ConfigEntry]:
    """Get all loaded SmartThings config entries."""
    entries = []
    for domain in ("smartthings", "smartthings2"):
        for entry in hass.config_entries.async_entries(domain):
            if entry.state == config_entries.ConfigEntryState.LOADED:
                entries.append(entry)
    return entries


class SamsungRemoteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Samsung TV Remote."""

    VERSION = 3

    def __init__(self) -> None:
        self._smartthings_entries: list[config_entries.ConfigEntry] = []
        self._selected_smartthings_entry: config_entries.ConfigEntry | None = None
        self._available_tvs: list[dict[str, str]] = []
        self._mode: str | None = None
        self._host: str | None = None
        self._port: int = DEFAULT_PORT
        self._mac: str | None = None
        self._token: str | None = None
        self._device_name: str = "Samsung TV"

    # ------------------------------------------------------------------
    # Step 1: choose connection mode
    # ------------------------------------------------------------------

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Initial step – choose Cloud or Local."""
        if user_input is not None:
            self._mode = user_input[CONF_CONNECTION_MODE]
            if self._mode == MODE_LOCAL:
                return await self.async_step_local()
            return await self.async_step_cloud()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_CONNECTION_MODE, default=MODE_LOCAL): vol.In(
                        {
                            MODE_LOCAL: "Local (WebSocket / LAN – no cloud)",
                            MODE_CLOUD: "Cloud (SmartThings API)",
                        }
                    ),
                }
            ),
        )

    # ------------------------------------------------------------------
    # Cloud path (original flow)
    # ------------------------------------------------------------------

    async def async_step_cloud(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Select SmartThings integration."""
        from .smartthings_bridge import get_smartthings_token

        errors: dict[str, str] = {}
        self._smartthings_entries = await _get_smartthings_entries(self.hass)

        if not self._smartthings_entries:
            return self.async_abort(reason="no_smartthings")

        if len(self._smartthings_entries) == 1:
            self._selected_smartthings_entry = self._smartthings_entries[0]
            token = await get_smartthings_token(self.hass, self._selected_smartthings_entry)
            if not token:
                return self.async_abort(reason="no_token")
            return await self.async_step_select_tv()

        if user_input is not None:
            selected_entry_id = user_input.get("smartthings_entry")
            self._selected_smartthings_entry = next(
                (e for e in self._smartthings_entries if e.entry_id == selected_entry_id),
                None,
            )
            if self._selected_smartthings_entry:
                token = await get_smartthings_token(
                    self.hass, self._selected_smartthings_entry
                )
                if not token:
                    errors["base"] = "no_token"
                else:
                    return await self.async_step_select_tv()
            else:
                errors["base"] = "invalid_entry"

        entry_options = {
            entry.entry_id: entry.title or f"SmartThings ({entry.domain})"
            for entry in self._smartthings_entries
        }

        return self.async_show_form(
            step_id="cloud",
            data_schema=vol.Schema(
                {vol.Required("smartthings_entry"): vol.In(entry_options)}
            ),
            errors=errors,
            description_placeholders={"count": str(len(self._smartthings_entries))},
        )

    async def async_step_select_tv(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Select a Samsung TV from SmartThings account."""
        from .smartthings_bridge import get_samsung_tvs_from_api

        errors: dict[str, str] = {}

        if not self._selected_smartthings_entry:
            return self.async_abort(reason="no_smartthings")

        if not self._available_tvs:
            self._available_tvs = await get_samsung_tvs_from_api(
                self.hass, self._selected_smartthings_entry
            )

        if not self._available_tvs:
            return self.async_abort(reason="no_tvs_found")

        if user_input is not None:
            device_id = user_input.get("device_id")
            selected_tv = next(
                (tv for tv in self._available_tvs if tv["id"] == device_id), None
            )
            if selected_tv:
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=selected_tv["name"],
                    data={
                        CONF_CONNECTION_MODE: MODE_CLOUD,
                        CONF_DEVICE_ID: device_id,
                        CONF_DEVICE_NAME: selected_tv["name"],
                        CONF_SMARTTHINGS_ENTRY_ID: self._selected_smartthings_entry.entry_id,
                    },
                )
            errors["base"] = "invalid_device"

        tv_options = {tv["id"]: tv["name"] for tv in self._available_tvs}
        return self.async_show_form(
            step_id="select_tv",
            data_schema=vol.Schema(
                {vol.Required("device_id"): vol.In(tv_options)}
            ),
            errors=errors,
            description_placeholders={"count": str(len(self._available_tvs))},
        )

    # ------------------------------------------------------------------
    # Local path
    # ------------------------------------------------------------------

    async def async_step_local(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Enter host / port / optional MAC & token for local control."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._host = user_input[CONF_HOST].strip()
            self._port = int(user_input.get(CONF_PORT, DEFAULT_PORT))
            self._mac = (user_input.get(CONF_MAC) or "").strip() or None
            self._token = (user_input.get(CONF_TOKEN) or "").strip() or None
            self._device_name = (user_input.get(CONF_DEVICE_NAME) or "Samsung TV").strip()

            # Unique ID based on host so the same TV cannot be added twice
            await self.async_set_unique_id(f"local_{self._host}")
            self._abort_if_unique_id_configured()

            # Try a quick connection / pairing
            try:
                from .local_bridge import LocalBridge

                bridge = LocalBridge(
                    self.hass,
                    host=self._host,
                    token=self._token,
                    port=self._port,
                    name="Home Assistant",
                    mac=self._mac,
                )
                await bridge.async_initialize()
                # Capture token if TV issued one
                if bridge.token:
                    self._token = bridge.token
                await bridge.async_close()
            except Exception as err:
                _LOGGER.warning("Local connection test failed: %s", err)
                errors["base"] = "cannot_connect"
                # Still allow creation – user may need to accept the popup first
                if "cannot_connect" in errors and user_input.get("force", False):
                    errors = {}

            if not errors:
                return self.async_create_entry(
                    title=f"{self._device_name} (Local)",
                    data={
                        CONF_CONNECTION_MODE: MODE_LOCAL,
                        CONF_HOST: self._host,
                        CONF_PORT: self._port,
                        CONF_TOKEN: self._token,
                        CONF_MAC: self._mac,
                        CONF_DEVICE_NAME: self._device_name,
                        CONF_DEVICE_ID: f"local_{self._host}",
                    },
                )

        return self.async_show_form(
            step_id="local",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): vol.All(
                        vol.Coerce(int), vol.Range(min=1, max=65535)
                    ),
                    vol.Optional(CONF_DEVICE_NAME, default="Samsung TV"): str,
                    vol.Optional(CONF_MAC): str,
                    vol.Optional(CONF_TOKEN): str,
                }
            ),
            errors=errors,
            description_placeholders={},
        )

    # ------------------------------------------------------------------
    # Options
    # ------------------------------------------------------------------

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        return SamsungRemoteOptionsFlow(config_entry)


class SamsungRemoteOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "scan_interval",
                        default=self.config_entry.options.get("scan_interval", 30),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
                }
            ),
        )
