"""Sensor platform for Google Fit."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import Coordinator
from .entity import GoogleFitEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="google_fit",
        name="steps",
        icon="mdi:walk",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    coordinator: Coordinator = entry_data.get("coordinator")
    async_add_devices(
        GoogleFitBlueprintSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class GoogleFitBlueprintSensor(GoogleFitEntity, SensorEntity):
    """Google Fit Template Sensor class."""

    def __init__(
        self,
        coordinator: Coordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialise the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    def _read_value(self) -> None:
        if self.coordinator.current_data is not None:
            self._attr_native_value = self.coordinator.current_data.get(
                self.entity_description.name
            )
            self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._read_value()
