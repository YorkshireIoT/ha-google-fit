"""API for Google Fit bound to Home Assistant OAuth."""
from datetime import datetime
from aiohttp import ClientSession
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google.oauth2.utils import OAuthClientAuthHandler
from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache

from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api_types import (
    FitService,
    FitnessData,
    FitnessObject,
    FitnessDataPoint,
    FitnessDataSource,
)
from .const import SLEEP_STAGE, ENTITY_DESCRIPTIONS


class AsyncConfigEntryAuth(OAuthClientAuthHandler):
    """Provide Google Fit authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        websession: ClientSession,
        oauth2Session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialise Google Fit Auth."""
        self.oauth_session = oauth2Session
        self.discovery_cache = SimpleDiscoveryCache()
        super().__init__(websession)

    @property
    def access_token(self) -> str:
        """Return the access token."""
        return self.oauth_session.token[CONF_ACCESS_TOKEN]

    async def check_scopes(self, hass: HomeAssistant) -> None:
        """Check the current scope access."""
        service = await self.get_resource(hass)

        def get_sources() -> FitnessDataSource:
            return service.users().dataSources().list(userId="me").execute()

        data_sources = await hass.async_add_executor_job(get_sources)

        available_sources = []
        for data_stream in data_sources.get("dataSource"):
            available_sources.append(data_stream.get("dataStreamId"))

        # Cycle through each of the required sources and check the current
        # auth gives access to them
        for entity in ENTITY_DESCRIPTIONS:
            if entity.source not in available_sources:
                raise ConfigEntryAuthFailed(
                    "Current authentication does not provide access to all required sensors."
                    + " Re-authentication required."
                )

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

    def __init__(self) -> None:
        """Cache Initialisation."""
        self._data = {}

    def get(self, url):
        """Cache Getter (if available)."""
        if url in self._data:
            return self._data[url]
        return None

    def set(self, url, content) -> None:
        """Cache Setter."""
        self._data[url] = content


class GoogleFitParse:
    """Parse raw data received from the Google Fit API."""

    data: FitnessData

    def __init__(self):
        """Initialise the data to base value and add a timestamp."""
        self.data = FitnessData(
            lastUpdate=datetime.now(),
            activeMinutes=None,
            calories=None,
            distance=None,
            heartMinutes=None,
            height=None,
            weight=None,
            steps=None,
            awakeSeconds=0,
            sleepSeconds=0,
            lightSleepSeconds=0,
            deepSleepSeconds=0,
            remSleepSeconds=0,
        )

    def _sum_points_int(self, response: FitnessObject) -> int:
        counter = 0
        for point in response.get("point"):
            value = point.get("value")[0].get("intVal")
            if value is not None:
                counter += value
        return counter

    def _sum_points_float(self, response: FitnessObject) -> float:
        counter = 0
        for point in response.get("point"):
            value = point.get("value")[0].get("fpVal")
            if value is not None:
                counter += value
        return round(counter, 2)

    def _get_first_data_point(self, response: FitnessDataPoint) -> float | None:
        value = None
        data_points = response.get("insertedDataPoint")
        if len(data_points) > 0:
            values = data_points[0].get("value")
            if len(values) > 0:
                data_point = values[0].get("fpVal")
                if data_point is not None:
                    value = round(data_point, 2)

        return value

    def _parse_object(self, request_id: str, response: FitnessObject):
        """Parse the given fit object from the API according to the passed request_id."""
        # Sensor types where data is returned as integer and needs summing
        if request_id in ["activeMinutes", "steps"]:
            self.data[request_id] = self._sum_points_int(response)
        # Sensor types where data is returned as float and needs summing
        elif request_id in ["calories", "distance", "heartMinutes"]:
            self.data[request_id] = self._sum_points_float(response)
        elif request_id in [
            "awakeSeconds",
            "sleepSeconds",
            "lightSleepSeconds",
            "deepSleepSeconds",
            "remSleepSeconds",
        ]:
            for point in response.get("point"):
                sleep_type = point.get("value")[0].get("intVal")
                start_time = point.get("startTimeNanos")
                end_time = point.get("endTimeNanos")
                # Sleep type 3 (out-of-bed is not support)
                if (
                    sleep_type is not None
                    and start_time is not None
                    and end_time is not None
                ):
                    sleep_stage = SLEEP_STAGE.get(sleep_type)
                    if sleep_stage is not None:
                        self.data[sleep_stage] += (
                            int(end_time) - int(start_time)
                        ) / 1000000000

            self.data["sleepSeconds"] += (
                self.data["lightSleepSeconds"]
                + self.data["deepSleepSeconds"]
                + self.data["remSleepSeconds"]
            )
        else:
            raise UpdateFailed(
                f"Unknown request ID specified for parsing: {request_id}"
            )

    def _parse_point(self, request_id: str, response: FitnessDataPoint):
        """Parse the given fit data point from the API according to the passed request_id."""
        # Sensor types where data is returned as integer and needs summing
        if request_id in ["height", "weight"]:
            self.data[request_id] = self._get_first_data_point(response)
        else:
            raise UpdateFailed(
                f"Unknown request ID specified for parsing: {request_id}"
            )

    def parse(
        self,
        request_id: str,
        fit_object: FitnessObject | None = None,
        fit_point: FitnessDataPoint | None = None,
    ) -> None:
        """Parse either (but not both) the given fit object or point according to request_id."""
        if fit_object is not None and fit_point is None:
            self._parse_object(request_id, fit_object)
        elif fit_object is None and fit_point is not None:
            self._parse_point(request_id, fit_point)
        else:
            raise UpdateFailed(
                "Invalid parse call."
                + "Either object must be None or point must be None. Not both or neither."
            )

    @property
    def fit_data(self) -> FitnessData:
        """Returns the local data. Should be called after parse."""
        return self.data
