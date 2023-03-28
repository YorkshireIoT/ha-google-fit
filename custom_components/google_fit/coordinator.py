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
    def current_data(self) -> FitnessData | None:
        """Return the current data, or None is data is not available."""
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

                def _get_data_changes(source: str) -> FitnessObject:
                    return (
                        service.users()
                        .dataSources()
                        .dataPointChanges()
                        .list(userId="me", dataSourceId=source)
                        .execute()
                    )

                def _sum_points_int(response: FitnessObject) -> int:
                    counter = 0
                    for point in response.get("point"):
                        value = point.get("value")[0].get("intVal")
                        if value is not None:
                            counter += value
                    return counter

                def _sum_points_float(response: FitnessObject) -> float:
                    counter = 0
                    for point in response.get("point"):
                        value = point.get("value")[0].get("fpVal")
                        if value is not None:
                            counter += value
                    return round(counter, 2)

                def _get_first_data_point(response: FitnessDataPoint) -> float | None:
                    value = None
                    data_points = response.get("insertedDataPoint")
                    if len(data_points) > 0:
                        values = data_points[0].get("value")
                        if len(values) > 0:
                            value = round(values[0].get("fpVal"), 2)

                    return value

                def parse_response(
                    request_id: str, response: FitnessObject | FitnessDataPoint
                ) -> None:
                    # Sensor types where data is returned as integer and needs summing
                    if request_id in ["activeMinutes", "steps"]:
                        received_data[request_id] = _sum_points_int(response)
                    # Sensor types where data is returned as float and needs summing
                    elif request_id in ["calories", "distance", "heartMinutes"]:
                        received_data[request_id] = _sum_points_float(response)
                    # Sensor types where data is returned as single float point (no summing)
                    elif request_id in ["height", "weight"]:
                        received_data[request_id] = _get_first_data_point(response)
                    else:
                        raise UpdateFailed(
                            f"Unknown request ID specified for parsing: {request_id}"
                        )

                dataset = self._get_interval()
                for entity in ENTITY_DESCRIPTIONS:
                    response = {}
                    if entity.data_key not in ["height", "weight"]:
                        response = await self.hass.async_add_executor_job(
                            _get_data, entity.source, dataset
                        )
                    else:
                        response = await self.hass.async_add_executor_job(
                            _get_data_changes, entity.source
                        )
                    parse_response(entity.data_key, response)

                self.fitness_data = received_data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
