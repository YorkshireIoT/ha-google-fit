"""TypeDefinition for Google Fit API"""
from datetime import datetime
from typing import TypedDict, Optional, Callable, Any

from googleapiclient.discovery import Resource
from googleapiclient.http import BatchHttpRequest


class FitService(Resource):
    """Service implementation for the Fit API."""

    users: Callable[[], Any]
    new_batch_http_request: Callable[[Callable[..., None]], BatchHttpRequest]


class FitnessData(TypedDict):
    """All the fitenss data retrieved from the API"""

    lastUpdate: datetime
    activeMinutes: Optional[int]
    calories: Optional[float]
    distance: Optional[float]
    heartMinutes: Optional[float]
    height: Optional[float]
    weight: Optional[float]
    steps: Optional[int]


class FitnessValue(TypedDict):
    """Representation of a the value of a single data point returned from the Google Fit API.
    See: https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.datasets.html#get
    """

    fpVal: Optional[float]
    intVal: Optional[int]
    stringVal: Optional[str]


class FitnessPoint(TypedDict):
    """Representation of a single data point returned from the Google Fit API.
    See: https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.datasets.html#get
    """

    dataTypeName: str
    endTimeNanos: str
    modifiedTimeMillis: str
    rawTimestampNanos: str
    startTimeNanos: str
    value: list[FitnessValue]


class FitnessObject(TypedDict):
    """Representation of the data returned from the Google Fit API.
    See: https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.datasets.html#get
    """

    dataSourceId: str
    maxEndTimeNs: str
    minStartTimeNs: str
    nextPageToken: str
    point: list[FitnessPoint]
