"""Config flow for Google Fit integration."""
from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleApiError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_TOKEN
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_entry_oauth2_flow

from .api_types import FitService
from .const import DEFAULT_ACCESS, DOMAIN


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle Google Fit OAuth2 authentication."""

    DOMAIN = DOMAIN
    VERSION = 2

    reauth_entry: ConfigEntry | None = None

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    @property
    def extra_authorize_data(self) -> dict[str, Any]:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "scope": " ".join(DEFAULT_ACCESS),
            # Add params to ensure we get back a refresh token
            "access_type": "offline",
            "prompt": "consent",
        }

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult:
        """Perform reauth upon an API authentication error."""
        _ = entry_data
        self.reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm reauth dialog."""
        if user_input is None:
            return self.async_show_form(step_id="reauth_confirm")  # type: ignore
        return await self.async_step_user()

    async def async_oauth_create_entry(self, data: dict[str, Any]) -> FlowResult:
        """Create an entry for the flow, or update existing entry."""
        if self.reauth_entry:
            self.hass.config_entries.async_update_entry(self.reauth_entry, data=data)
            await self.hass.config_entries.async_reload(self.reauth_entry.entry_id)
            return self.async_abort(reason="reauth_successful")

        credentials = Credentials(data[CONF_TOKEN][CONF_ACCESS_TOKEN])

        def _get_profile() -> dict[str, Any]:
            """Get profile from inside the executor."""
            lib = build("oauth2", "v2", credentials=credentials)
            user_info = lib.userinfo().get().execute()  # pylint: disable=no-member
            return user_info

        def _check_fit_access() -> FitService:
            lib = build(
                "fitness",
                "v1",
                credentials=credentials,
                static_discovery=False,
            )
            sources = (
                lib.users()  # pylint: disable=no-member
                .dataSources()
                .list(userId="me")
                .execute()
            )
            return sources

        try:
            (await self.hass.async_add_executor_job(_check_fit_access))
            email = (await self.hass.async_add_executor_job(_get_profile))["email"]
        except GoogleApiError as ex:
            self.logger.error("API Access Error: %s", ex.reason)
            return self.async_abort(
                reason="access_error", description_placeholders={"reason": ex.reason}
            )

        await self.async_set_unique_id(email)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=email, data=data)
