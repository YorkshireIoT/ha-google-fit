"""API for Google Fit bound to Home Assistant OAuth."""
from aiohttp import ClientSession
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google.oauth2.utils import OAuthClientAuthHandler
from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache

from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.helpers import config_entry_oauth2_flow

from .api_types import FitService


class AsyncConfigEntryAuth(OAuthClientAuthHandler):
    """Provide Google Fit authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        websession: ClientSession,
        oauth2Session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize Google Fit Auth."""
        self.oauth_session = oauth2Session
        self.discovery_cache = SimpleDiscoveryCache()
        super().__init__(websession)

    @property
    def access_token(self) -> str:
        """Return the access token."""
        return self.oauth_session.token[CONF_ACCESS_TOKEN]

    async def check_and_refresh_token(self) -> str:
        """Check the token."""
        await self.oauth_session.async_ensure_token_valid()
        return self.access_token

    async def get_resource(self, hass: HomeAssistant) -> FitService:
        """Get current resource."""

        try:
            credentials = Credentials(await self.check_and_refresh_token())
        except RefreshError as ex:
            self.oauth_session.config_entry.async_start_reauth(self.oauth_session.hass)
            raise ex

        def get_fitness() -> FitService:
            return build(
                "fitness",
                "v1",
                credentials=credentials,
                cache=self.discovery_cache,
                static_discovery=False,
            )

        return await hass.async_add_executor_job(get_fitness)


class SimpleDiscoveryCache(Cache):
    """A very simple discovery cache."""

    def __init__(self):
        self._data = dict([])

    def get(self, url):
        if url in self._data:
            return self._data[url]

    def set(self, url, content):
        self._data[url] = content
