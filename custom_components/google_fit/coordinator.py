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
    data: FitnessData = None  # type: ignore

    def __init__(
        self,
        hass: HomeAssistant,
        auth: AsyncConfigEntryAuth,
        config: ConfigEntry,
    ) -> None:
        """Initialize."""
        self._auth = auth
        self._config = config
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    def _get_request(self, service: FitService, source: str):
        # Required type is in nanoseconds since Epoch in
        # format "{start}-{end}"
        start = int(datetime.today().date().strftime("%s")) * 1000000000
        now = int(datetime.today().timestamp() * 1000000000)
        dataset = f"${start}-{now}"
        return (
            service.users()
            .dataSources()
            .datasets()
            .get(userId="me", dataSourceId=source, datasetId=dataset)
        )

    async def _async_update_data(self) -> FitService | None:
        """Update data via library."""

        try:
            async with async_timeout.timeout(30):
                if self.data is None:
                    service = await self._auth.get_resource(self.hass)

                    recevied_data = FitnessData(
                        lastUpdate=datetime.now(),
                        activeMinutes=None,
                        calories=None,
                        distance=None,
                        heartMinutes=None,
                        height=None,
                        weight=None,
                        steps=None,
                    )

                    def parse_response(
                        request_id: str, response: FitnessObject, exception
                    ):
                        if exception is not None:
                            raise UpdateFailed(
                                f"Error communicating with API: {exception}"
                            ) from exception
                        else:
                            if request_id == "steps":
                                steps = 0
                                for point in response.get("point"):
                                    value = point.get("value")[0].get("intVal")
                                    if value is not None:
                                        steps += value
                                recevied_data["steps"] = steps
                            else:
                                raise UpdateFailed(
                                    f"Unknown batch request ID in callback: {request_id}"
                                )

                    # Build a Batch HTTP Request
                    batch = service.new_batch_http_request(callback=parse_response)  # type: ignore
                    batch.add(
                        self._get_request(
                            service,
                            SOURCE_STEPS,
                        ),
                        "steps",
                    )

                    await batch.execute()
                    self.data = recevied_data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
