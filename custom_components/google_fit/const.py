"""Constants for Google Fit."""
from __future__ import annotations
from typing import Final
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

# Base Component Values
NAME: Final = "Google Fit"
DOMAIN: Final = "google_fit"
MANUFACTURER: Final = "Google, Inc."

# Required Scopes
DATA_AUTH: Final = "auth"
DEFAULT_ACCESS = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/fitness.activity.read",
    "https://www.googleapis.com/auth/fitness.body.read",
    "https://www.googleapis.com/auth/fitness.nutrition.read",
]

ATTRIBUTION: Final = "json"
ISSUE_URL: Final = "https://github.com/YorkshireIoT/ha-google-fit/issues"
CONF_UPDATE_INTERVAL: Final = "update_interval"

DATA_CLIENT: Final = "client"
DATA_COORDINATOR: Final = "coordinator"

# Fitness Source IDs
SOURCE_STEPS: Final = (
    "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
)
