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
from .api import AsyncConfigEntryAuth
from .api_types import FitService, FitnessData, FitnessObject
from .const import DOMAIN, LOGGER, SOURCE_STEPS


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
    def current_data(self) -> FitnessData | None:
        """Return the current data, or None is data is not available."""
        if self.fitness_data is None:
            return None
        else:
            return self.fitness_data

    def _get_interval(self):
        start = int(datetime.today().date().strftime("%s")) * 1000000000
        now = int(datetime.today().timestamp() * 1000000000)
        return f"{start}-{now}"

    async def _async_update_data(self) -> FitService | None:
        """Update data via library."""

        try:
            async with async_timeout.timeout(30):
                service = await self._auth.get_resource(self.hass)

                received_data = FitnessData(
                    lastUpdate=datetime.now(),
                    activeMinutes=None,
                    calories=None,
                    distance=None,
                    heartMinutes=None,
                    height=None,
                    weight=None,
                    steps=None,
                )

                def _get_data(source: str, dataset: str) -> FitnessObject:
                    return (
                        service.users()
                        .dataSources()
                        .datasets()
                        .get(userId="me", dataSourceId=source, datasetId=dataset)
                        .execute()
                    )

                def parse_response(request_id: str, response: FitnessObject) -> None:
                    if request_id == "steps":
                        steps = 0
                        for point in response.get("point"):
                            value = point.get("value")[0].get("intVal")
                            if value is not None:
                                steps += value
                        received_data["steps"] = steps
                        LOGGER.debug("Step retrieval successful. Got %d steps.", steps)
                    else:
                        raise UpdateFailed(
                            f"Unknown batch request ID in callback: {request_id}"
                        )

                dataset = self._get_interval()
                response = await self.hass.async_add_executor_job(
                    _get_data, SOURCE_STEPS, dataset
                )
                parse_response("steps", response)
                self.fitness_data = received_data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
