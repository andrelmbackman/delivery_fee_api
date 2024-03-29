import pytest
from app.delivery_fee import is_rush_hour


@pytest.mark.parametrize(
    "time",
    [
        "2024-01-24T12:30:45Z",
        "2024-01-26T19:00:01.000Z",  # one second after rush hour
        "2024-01-26T19:00:00.000Z",  # one millisecond after rush hour
        "2024-01-26T14:59:59.000Z",  # one second before rush hour
        "2024-01-26T14:59:59.999Z",  # one millisecond before rush hour
    ],
)
def test_time_formats_not_rush_hour(time: str):
    """Test that is_rush_hour does not return false positives."""
    assert not is_rush_hour(time)


@pytest.mark.parametrize(
    "time",
    [
        "2024-01-26T17:00:45Z",
        "2024-01-26T12:00:45-05:00",
        "2024-01-26T09:00:45-08:00",
        "2024-01-26T18:00:45+01:00",
        "2024-01-27T02:00:45+09:00",
        "2024-01-26T15:00:00.000Z",  # right on rush hour
        "2024-01-26T18:59:59.999Z",  # right before rush hour ends
    ],
)
def test_time_zones_rush_hour(time: str):
    """Test that is_rush_hour returns true, even a millisecond before it stops."""
    assert is_rush_hour(time)


@pytest.mark.parametrize(
    "time",
    [
        "2024-01-22T17:00:45Z",
        "2024-01-22T18:00:45+01:00",
        "2024-01-22T19:00:45+02:00",
        "2024-01-22T20:00:45+03:00",
        "2024-01-22T21:00:45+04:00",
        "2024-01-22T22:00:45+05:00",
        "2024-01-22T23:00:45+06:00",
        "2024-01-22T00:00:45+07:00",
        "2024-01-22T01:00:45+08:00",
        "2024-01-22T02:00:45+09:00",
        "2024-01-22T03:00:45+10:00",
        "2024-01-22T04:00:45+11:00",
        "2024-01-22T05:00:45+12:00",
        "2024-01-22T16:00:45-01:00",
        "2024-01-22T15:00:45-02:00",
        "2024-01-22T14:00:45-03:00",
        "2024-01-22T13:00:45-04:00",
        "2024-01-22T12:00:45-05:00",
        "2024-01-22T11:00:45-06:00",
        "2024-01-22T10:00:45-07:00",
        "2024-01-22T09:00:45-08:00",
        "2024-01-22T08:00:45-09:00",
        "2024-01-22T07:00:45-10:00",
        "2024-01-22T06:00:45-11:00",
        "2024-01-22T05:00:45-12:00",
    ],
)
def test_all_timezones_not_rush_hour(time: str):
    """Test is_rush_hour with all timezone offsets, ensure no false positives."""
    assert not is_rush_hour(time)


@pytest.mark.parametrize(
    "time",
    [
        "2024-01-26T17:00:45Z",
        "2024-01-26T18:00:45+01:00",
        "2024-01-26T19:00:45+02:00",
        "2024-01-26T20:00:45+03:00",
        "2024-01-26T21:00:45+04:00",
        "2024-01-26T22:00:45+05:00",
        "2024-01-26T23:00:45+06:00",
        "2024-01-27T00:00:45+07:00",
        "2024-01-27T01:00:45+08:00",
        "2024-01-27T02:00:45+09:00",
        "2024-01-27T03:00:45+10:00",
        "2024-01-27T04:00:45+11:00",
        "2024-01-27T05:00:45+12:00",
        "2024-01-26T16:00:45-01:00",
        "2024-01-26T15:00:45-02:00",
        "2024-01-26T14:00:45-03:00",
        "2024-01-26T13:00:45-04:00",
        "2024-01-26T12:00:45-05:00",
        "2024-01-26T11:00:45-06:00",
        "2024-01-26T10:00:45-07:00",
        "2024-01-26T09:00:45-08:00",
        "2024-01-26T08:00:45-09:00",
        "2024-01-26T07:00:45-10:00",
        "2024-01-26T06:00:45-11:00",
        "2024-01-26T05:00:45-12:00",
    ],
)
def test_all_time_zones_rush_hour(time: str):
    """Test is_rush_hour with all timezone offsets, ensure no false negatives."""
    assert is_rush_hour(time)


@pytest.mark.parametrize(
    "time",
    [
        "2024-01-26T17:00:45.000Z",
        "2024-01-26T17:00:45Z",
        "2024-01-26T17:00:45+00",
        "2024-01-26T17:00:45+0000",
        "2024-01-26T17:00:45+00:00",
        "2024-01-26T17:00:45.000+00",
        "2024-01-26T17:00:45.000+0000",
        "2024-01-26T17:00:45.000+00:00",
        "2024-01-26T17:00:45-00",
        "2024-01-26T17:00:45-0000",
        "2024-01-26T17:00:45-00:00",
        "2024-01-26T17:00:45.000-00",
        "2024-01-26T17:00:45.001-0000",
        "2024-01-26T17:00:45.999-00:00",
        "2024-01-26T17:00:45.99-00:00",
        "2024-01-26T17:00:45.9-00:00",
    ],
)
def test_iso_format_rush_hour(time: str):
    """Test is_rush_hour for false negatives, with various precision and timezone offset formats."""
    assert is_rush_hour(time)


@pytest.mark.parametrize(
    "time",
    [
        "24-01-26T16:30:45Z",
        "2024-01-26T16:00:99",
        "2024-01-2616:00:00Z",
        "2024-99-99T14:59:59Z",
    ],
)
def test_invalid_time_returns_false(time: str):
    """Test if is_rush_hour returns false when the argument is invalid."""
    assert not is_rush_hour(time)


def test_none_time_returns_false():
    assert not is_rush_hour(None)
