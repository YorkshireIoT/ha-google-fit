"""DataUpdateCoordinator for Google Fit."""
from __future__ import annotations

from datetime import timedelta, datetime
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session
from .api import AsyncConfigEntryAuth, GoogleFitParse
from .api_types import FitService, FitnessData, FitnessObject, FitnessDataPoint
from .const import DOMAIN, LOGGER, ENTITY_DESCRIPTIONS


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class Coordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    _auth: AsyncConfigEntryAuth
    _config: ConfigEntry
    fitness_data: FitnessData | None = None

    def __init__(
        self,
        hass: HomeAssistant,
        auth: AsyncConfigEntryAuth,
        config: ConfigEntry,
    ) -> None:
        """Initialise."""
        self._auth = auth
        self._config = config
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )

    @property
    def oauth_session(self) -> OAuth2Session | None:
        """Returns the OAuth Session associated with the coordinator, or None if not available."""
        if self._auth is None:
            return None
        return self._auth.oauth_session

    @property
    def current_data(self) -> FitnessData | None:
        """Return the current data, or None is data is not available."""
        return self.fitness_data

    def _get_interval(self, midnight_reset: bool = True):
        start = 0
        if midnight_reset:
            start = (
                int(
                    datetime.combine(
                        datetime.today().date(), datetime.min.time()
                    ).timestamp()
                )
                * 1000000000
            )
        # Make start time exactly 24 hours ago
        else:
            start = (int(datetime.today().timestamp()) - 60 * 60 * 24) * 1000000000
        now = int(datetime.today().timestamp() * 1000000000)
        return f"{start}-{now}"

    async def _async_update_data(self) -> FitService | None:
        """Update data via library."""

        try:
            async with async_timeout.timeout(30):
                service = await self._auth.get_resource(self.hass)
                parser = GoogleFitParse()

                def _get_data(source: str, dataset: str) -> FitnessObject:
                    return (
                        service.users()
                        .dataSources()
                        .datasets()
                        .get(userId="me", dataSourceId=source, datasetId=dataset)
                        .execute()
                    )

                def _get_data_changes(source: str) -> FitnessDataPoint:
                    return (
                        service.users()
                        .dataSources()
                        .dataPointChanges()
                        .list(userId="me", dataSourceId=source)
                        .execute()
                    )

                fetched_sleep = False
                for entity in ENTITY_DESCRIPTIONS:
                    if entity.data_key in [
                        "activeMinutes",
                        "calories",
                        "distance",
                        "heartMinutes",
                        "steps",
                    ]:
                        dataset = self._get_interval()
                        response = await self.hass.async_add_executor_job(
                            _get_data, entity.source, dataset
                        )
                        parser.parse(entity.data_key, fit_object=response)
                    elif entity.data_key in [
                        "awakeSeconds",
                        "sleepSeconds",
                        "lightSleepSeconds",
                        "deepSleepSeconds",
                        "remSleepSeconds",
                    ]:
                        # Only need to call once to get all different sleep segments
                        if fetched_sleep is False:
                            dataset = self._get_interval(False)
                            response = await self.hass.async_add_executor_job(
                                _get_data, entity.source, dataset
                            )
                            fetched_sleep = True
                            parser.parse(entity.data_key, fit_object=response)
                    # Height and weight
                    else:
                        response = await self.hass.async_add_executor_job(
                            _get_data_changes, entity.source
                        )
                        parser.parse(entity.data_key, fit_point=response)

                self.fitness_data = parser.fit_data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
