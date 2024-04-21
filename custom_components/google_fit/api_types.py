"""TypeDefinition for Google Fit API."""

from datetime import datetime, timedelta
from typing import TypedDict, Any
from collections.abc import Callable
from dataclasses import dataclass, field
from homeassistant.components.sensor import SensorEntityDescription
from googleapiclient.discovery import Resource
from googleapiclient.http import BatchHttpRequest


class FitService(Resource):
    """Service implementation for the Fit API."""

    users: Callable[[], Any]
    new_batch_http_request: Callable[[Callable[..., None]], BatchHttpRequest]


@dataclass
class FitFloatSensor:
    """Represents a sensor with floating-point precision, e.g. height."""

    value: float | None = None
    attributes: dict[str, int | float | str] = field(
        default_factory=dict[str, int | float | str]
    )


@dataclass
class FitIntegerSensor:
    """Represents a sensor with integer precision, e.g. steps."""

    value: int | None = None
    attributes: dict[str, int | float | str] = field(
        default_factory=dict[str, int | float | str]
    )


@dataclass
class FitnessData:
    """All the fitness data retrieved from the API."""

    lastUpdate: datetime = datetime.now()
    activeMinutes: FitFloatSensor = field(default_factory=FitFloatSensor)
    calories: FitFloatSensor = field(default_factory=FitFloatSensor)
    basalMetabolicRate: FitFloatSensor = field(default_factory=FitFloatSensor)
    distance: FitFloatSensor = field(default_factory=FitFloatSensor)
    heartMinutes: FitFloatSensor = field(default_factory=FitFloatSensor)
    height: FitFloatSensor = field(default_factory=FitFloatSensor)
    weight: FitFloatSensor = field(default_factory=FitFloatSensor)
    bodyFat: FitFloatSensor = field(default_factory=FitFloatSensor)
    bodyTemperature: FitFloatSensor = field(default_factory=FitFloatSensor)
    steps: FitIntegerSensor = field(default_factory=FitIntegerSensor)
    awakeSeconds: FitFloatSensor = field(default_factory=FitFloatSensor)
    sleepSeconds: FitFloatSensor = field(default_factory=FitFloatSensor)
    lightSleepSeconds: FitFloatSensor = field(default_factory=FitFloatSensor)
    deepSleepSeconds: FitFloatSensor = field(default_factory=FitFloatSensor)
    remSleepSeconds: FitFloatSensor = field(default_factory=FitFloatSensor)
    heartRate: FitFloatSensor = field(default_factory=FitFloatSensor)
    heartRateResting: FitFloatSensor = field(default_factory=FitFloatSensor)
    bloodPressureSystolic: FitFloatSensor = field(default_factory=FitFloatSensor)
    bloodPressureDiastolic: FitFloatSensor = field(default_factory=FitFloatSensor)
    bloodGlucose: FitFloatSensor = field(default_factory=FitFloatSensor)
    hydration: FitFloatSensor = field(default_factory=FitFloatSensor)
    oxygenSaturation: FitFloatSensor = field(default_factory=FitFloatSensor)

    def get(self, attribute_name: str) -> FitIntegerSensor | FitFloatSensor:
        """Get the value of the specified attribute."""
        if attribute_name not in self.__dataclass_fields__:
            raise KeyError(f"Invalid attribute for FitnessData: {attribute_name}")

        return self.__dataclass_fields__[attribute_name]

    def add_field(
        self, attribute_name: str, key: str, value: int | float | str
    ) -> None:
        """Add an additional field key, value pair to the sensor attributes list."""
        if attribute_name not in self.__dataclass_fields__:
            raise KeyError(f"Invalid attribute for FitnessData: {attribute_name}")

        sensorDict: FitFloatSensor | FitIntegerSensor = self.__dataclass_fields__[
            attribute_name
        ]

        sensorDict.attributes[key] = value

    def set(self, attribute_name: str, value: int | float) -> None:
        """Set the value of the specified attribute."""
        if attribute_name not in self.__dataclass_fields__:
            raise KeyError(f"Invalid attribute for FitnessData: {attribute_name}")

        sensorDict: FitFloatSensor | FitIntegerSensor = self.__dataclass_fields__[
            attribute_name
        ]
        if isinstance(sensorDict, FitFloatSensor) and isinstance(value, float):
            sensorDict.value = value
        elif isinstance(sensorDict, FitIntegerSensor) and isinstance(value, int):
            sensorDict.value = value
        else:
            raise TypeError(
                f"Cannot set value of type {value} to underlying type {type(sensorDict)}."
            )


class FitnessValue(TypedDict):
    """Representation of a the value of a single data point returned from the Google Fit API.

    See:
    https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.datasets
    """

    fpVal: float | None
    intVal: int | None
    stringVal: str | None


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


class FitnessDataStream(TypedDict):
    """Minimal representation of a data source returned from the Google Fit API.

    See:
    https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.html#list
    """

    dataStreamName: str
    dataStreamId: str
    type: str


class FitnessDataSource(TypedDict):
    """Minimal representation of a data source returned from the Google Fit API.

    See:
    https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.dataSources.html#list
    """

    dataSource: list[FitnessDataStream]


class FitnessSession(TypedDict):
    """Representation of a single session returned in response from Google Fit API.

    See:
    https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.sessions.html#list
    """

    activeTimeMillis: str
    activityType: int
    description: str
    endTimeMillis: str
    id: str
    modifiedTimeMillis: str
    name: str
    startTimeMillis: str


class FitnessSessionResponse(TypedDict):
    """Representation of a session response returned from the Google Fit API.

    See:
    https://googleapis.github.io/google-api-python-client/docs/dyn/fitness_v1.users.sessions.html#list
    """

    deletedSession: None
    hasMoreData: None
    nextPageToken: str | None
    session: list[FitnessSession]


class FitnessSensorField(TypedDict):
    index: int


class FitnessSensorEnumField(FitnessSensorField):
    enum: dict[int, str]


@dataclass  # type: ignore
class GoogleFitSensorDescription(SensorEntityDescription):
    """Extends Sensor Description types to add necessary component values."""

    data_key: str = "undefined"
    source: str = "undefined"
    is_int: bool = False  # If true, data is an integer. Otherwise, data is a float
    infrequent_update: bool = False
    enum_fields: dict[str, FitnessSensorEnumField] = field(
        default_factory=dict[str, FitnessSensorEnumField]
    )


@dataclass  # type: ignore
class SumPointsSensorDescription(GoogleFitSensorDescription):
    """Represents a sensor where the values are summed over a set time period."""

    # Sums points over this time period (in seconds). If period is 0, points will
    # be summed for that day (i.e. since midnight)
    period_seconds: int = 0

    # Defines if this is a sleep type sensor. Must have sleep stage enum as part of data
    is_sleep: bool = False


@dataclass  # type: ignore
class LastPointSensorDescription(GoogleFitSensorDescription):
    """Represents a sensor which just fetches the latest available data point."""

    # The index at which to fetch the data point. Normally 0 but bloodPressureDiastolic
    # has index 1 for example
    index: int = 0


@dataclass  # type: ignore
class SumSessionSensorDescription(GoogleFitSensorDescription):
    """Represents a sensor which just fetches the latest available data point."""

    # The Google Fit defined activity ID
    activity_id: int = 0

    # The period over which to sum
    period: timedelta = timedelta(days=1)
