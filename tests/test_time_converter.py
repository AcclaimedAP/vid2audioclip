import pytest
from src.utils.time_converter import TimeConverter

class TestTimeConverter:
    def test_time_to_seconds_minutes_seconds(self):
        assert TimeConverter.time_to_seconds("5:05.5") == 305.5
        assert TimeConverter.time_to_seconds("5:05,5") == 305.5
        assert TimeConverter.time_to_seconds("1:30") == 90

    def test_time_to_seconds_hours_minutes_seconds(self):
        assert TimeConverter.time_to_seconds("1:30:05.5") == 5405.5
        assert TimeConverter.time_to_seconds("1:30:05,5") == 5405.5

    def test_time_to_seconds_only_seconds(self):
        assert TimeConverter.time_to_seconds("5.5") == 5.5
        assert TimeConverter.time_to_seconds("5,5") == 5.5

    def test_invalid_time_format(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            TimeConverter.time_to_seconds("invalid")
        with pytest.raises(ValueError, match="Invalid time format"):
            TimeConverter.time_to_seconds("5:5:5:5")
        with pytest.raises(ValueError, match="Time cannot be negative"):
            TimeConverter.time_to_seconds("-1:30")
        with pytest.raises(ValueError, match="Invalid time format"):
            TimeConverter.time_to_seconds("abc:def")

    def test_seconds_to_time(self):
        assert TimeConverter.seconds_to_time(305.5) == "5:05.5"
        assert TimeConverter.seconds_to_time(5405.5) == "1:30:05.5"
        assert TimeConverter.seconds_to_time(5.5) == "5.5"

    def test_seconds_to_time_invalid(self):
        with pytest.raises(ValueError):
            TimeConverter.seconds_to_time(-5) 