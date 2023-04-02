"""TypeDefinition for Google Fit API."""
from datetime import datetime
from typing import TypedDict, Optional, Any
from collections.abc import Callable
from dataclasses import dataclass
from homeassistant.components.sensor import SensorEntityDescription
from googleapiclient.discovery import Resource
from googleapiclient.http import BatchHttpRequest


class FitService(Resource):
    """Service implementation for the Fit API."""

    users: Callable[[], Any]
    new_batch_http_request: Callable[[Callable[..., None]], BatchHttpRequest]


class FitnessData(TypedDict):
    """All the fitness data retrieved from the API."""

    lastUpdate: datetime
    activeMinutes: Optional[float]
    calories: Optional[float]
    distance: Optional[float]
    heartMinutes: Optional[float]
    height: Optional[float]
    weight: Optional[float]
    steps: Optional[int]


class FitnessValue(TypedDict):
    """Representation of a the value of a single data point returned from the Google Fit API.

    See:
    https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.datasets
    """

    fpVal: Optional[float]
    intVal: Optional[int]
    stringVal: Optional[str]


class FitnessPoint(TypedDict):
    """Representation of a single data point returned from the Google Fit API.

    See:
    https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.datasets
    """

    dataTypeName: str
    endTimeNanos: str
    modifiedTimeMillis: str
    rawTimestampNanos: str
    startTimeNanos: str
    value: list[FitnessValue]


class FitnessObject(TypedDict):
    """Representation of the data returned from the Google Fit API.

    See:
    https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.datasets
    """

    dataSourceId: str
    maxEndTimeNs: str
    minStartTimeNs: str
    nextPageToken: str
    point: list[FitnessPoint]


class FitnessDataPoint(TypedDict):
    """Representation of a data point change returned from the Google Fit API.

    See:
    https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.dataPointChanges
    """

    dataSourceId: str
    deletedDataPoint: list[FitnessPoint]
    insertedDataPoint: list[FitnessPoint]
    nextPageToken: str


@dataclass
class GoogleFitSensorDescription(SensorEntityDescription):
    """Extends Sensor Description types to add necessary component values."""

    data_key: str = "undefined"
    source: str = "undefined"
