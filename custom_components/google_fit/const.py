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


SETTING_INTERVAL_OPTION_NONE = "Never"
SETTING_INTERVAL_OPTION_10 = "10 seconds"
SETTING_INTERVAL_OPTION_30 = "30 seconds"
SETTING_INTERVAL_OPTION_60 = "60 seconds"
SETTING_INTERVAL_OPTION_120 = "120 seconds"
SETTING_INTERVAL_OPTION_300 = "300 seconds"
SETTING_INTERVAL_OPTIONS = [
    SETTING_INTERVAL_OPTION_NONE,
    SETTING_INTERVAL_OPTION_10,
    SETTING_INTERVAL_OPTION_30,
    SETTING_INTERVAL_OPTION_60,
    SETTING_INTERVAL_OPTION_120,
    SETTING_INTERVAL_OPTION_300,
]
SETTING_INTERVAL_DEFAULT_OPTION = SETTING_INTERVAL_OPTION_60
SETTING_INTERVAL_MAP = dict(
    {
        SETTING_INTERVAL_OPTION_NONE: None,
        SETTING_INTERVAL_OPTION_10: 10,
        SETTING_INTERVAL_OPTION_30: 30,
        SETTING_INTERVAL_OPTION_60: 60,
        SETTING_INTERVAL_OPTION_120: 120,
        SETTING_INTERVAL_OPTION_300: 300,
    }
)

# Fitness Source IDs
SOURCE_STEPS: Final = (
    "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
)
