"""Constants for Google Fit."""
from __future__ import annotations
from typing import Final
from logging import Logger, getLogger
from homeassistant.components.sensor import (
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.const import UnitOfTime, UnitOfLength, UnitOfMass

from .api_types import GoogleFitSensorDescription

LOGGER: Logger = getLogger(__package__)

# Base Component Values
NAME: Final = "Google Fit"
DOMAIN: Final = "google_fit"
MANUFACTURER: Final = "Google, Inc."

# Required Scopes
DEFAULT_ACCESS = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/fitness.activity.read",
    "https://www.googleapis.com/auth/fitness.body.read",
    "https://www.googleapis.com/auth/fitness.nutrition.read",
    "https://www.googleapis.com/auth/fitness.location.read",
]


ENTITY_DESCRIPTIONS = (
    GoogleFitSensorDescription(
        key="google_fit",
        name="Active Minutes Daily",
        icon="mdi:timer",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.DURATION,
        source="derived:com.google.active_minutes:com.google.android.gms:merge_active_minutes",
        data_key="activeMinutes",
    ),
    GoogleFitSensorDescription(
        key="google_fit",
        name="Calories Burnt Daily",
        icon="mdi:fire",
        native_unit_of_measurement="kcal",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=None,
        source="derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended",  # pylint: disable=line-too-long
        data_key="calories",
    ),
    GoogleFitSensorDescription(
        key="google_fit",
        name="Distance Travelled Daily",
        icon="mdi:run",
        native_unit_of_measurement=UnitOfLength.METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.DISTANCE,
        source="derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta",
        data_key="distance",
    ),
    GoogleFitSensorDescription(
        key="google_fit",
        name="Heart Points Daily",
        icon="mdi:heart",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=None,
        source="derived:com.google.heart_minutes:com.google.android.gms:merge_heart_minutes",
        data_key="heartMinutes",
    ),
    GoogleFitSensorDescription(
        key="google_fit",
        name="Height",
        icon="mdi:ruler",
        native_unit_of_measurement=UnitOfLength.METERS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DISTANCE,
        source="derived:com.google.height:com.google.android.gms:merge_height",
        data_key="height",
    ),
    GoogleFitSensorDescription(
        key="google_fit",
        name="Weight",
        icon="mdi:scale-bathroom",
        native_unit_of_measurement=UnitOfMass.KILOGRAMS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.WEIGHT,
        source="derived:com.google.weight:com.google.android.gms:merge_weight",
        data_key="weight",
    ),
    GoogleFitSensorDescription(
        key="google_fit",
        name="Steps Daily",
        icon="mdi:walk",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=None,
        source="derived:com.google.step_count.delta:com.google.android.gms:estimated_steps",
        data_key="steps",
    ),
)
