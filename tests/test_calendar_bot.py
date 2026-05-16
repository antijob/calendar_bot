import os
import tempfile
from datetime import datetime, timezone, timedelta
import pytest
from unittest.mock import patch, MagicMock

# Import functions from calendar_bot
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from calendar_bot import _read_secret, escape_markdown_v2, filter_events


class TestReadSecret:
    """Test _read_secret function for env var and file reading."""
    
    def test_read_secret_from_env_var(self):
        """Should read from env var when *_FILE not set."""
        with patch.dict(os.environ, {"TEST_VAR": "secret_value"}):
            result = _read_secret("TEST_VAR")
            assert result == "secret_value"
    
    def test_read_secret_from_file(self):
        """Should read from file when *_FILE env var is set."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("file_secret_value")
            f.flush()
            temp_file = f.name
        
        try:
            with patch.dict(os.environ, {"TEST_VAR_FILE": temp_file}):
                result = _read_secret("TEST_VAR")
                assert result == "file_secret_value"
        finally:
            os.unlink(temp_file)
    
    def test_read_secret_file_with_trailing_whitespace(self):
        """Should strip trailing whitespace from file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("secret_with_spaces\n\n  ")
            f.flush()
            temp_file = f.name
        
        try:
            with patch.dict(os.environ, {"TEST_VAR_FILE": temp_file}):
                result = _read_secret("TEST_VAR")
                assert result == "secret_with_spaces"
        finally:
            os.unlink(temp_file)
    
    def test_read_secret_returns_none_when_not_found(self):
        """Should return None when var and file not found."""
        with patch.dict(os.environ, {}, clear=True):
            result = _read_secret("NONEXISTENT_VAR")
            assert result is None
    
    def test_read_secret_file_takes_priority(self):
        """Should prefer file over env var when both exist."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("file_value")
            f.flush()
            temp_file = f.name
        
        try:
            with patch.dict(os.environ, {"TEST_VAR": "env_value", "TEST_VAR_FILE": temp_file}):
                result = _read_secret("TEST_VAR")
                assert result == "file_value"
        finally:
            os.unlink(temp_file)


class TestEscapeMarkdownV2:
    """Test escape_markdown_v2 function."""
    
    def test_escape_special_chars(self):
        """Should escape all MarkdownV2 special characters."""
        text = "_*[]()~`>#+-=|{}.!"
        result = escape_markdown_v2(text)
        assert result == r"\_\*\[\]\(\)\~\`\>\#\+\-\=\|\{\}\.\!"
    
    def test_preserve_normal_text(self):
        """Should not escape normal alphanumeric text."""
        text = "Hello World 123"
        result = escape_markdown_v2(text)
        assert result == "Hello World 123"
    
    def test_escape_mixed_text(self):
        """Should escape special chars but preserve normal text."""
        text = "Test [link](url) with *bold*"
        result = escape_markdown_v2(text)
        assert result == r"Test \[link\]\(url\) with \*bold\*"
    
    def test_empty_string(self):
        """Should handle empty string."""
        result = escape_markdown_v2("")
        assert result == ""


class TestFilterEvents:
    """Test filter_events function for correct date-based filtering."""

    BASE_TIME = datetime(2026, 5, 16, 12, 0, tzinfo=timezone.utc)
    
    def get_base_time(self):
        """Get a fixed UTC time for consistent testing."""
        return self.BASE_TIME
    
    def create_event(self, title, days_offset=0, hours_offset=0):
        """Create a mock event with given offset from now."""
        event_time = self.get_base_time() + timedelta(days=days_offset, hours=hours_offset)
        iso_time = event_time.isoformat()
        return {
            "id": f"event_{days_offset}",
            "summary": title,
            "start": {"dateTime": iso_time},
            "end": {"dateTime": (event_time + timedelta(hours=1)).isoformat()}
        }
    
    def test_filter_events_tomorrow(self):
        """Should filter events for 1 day ahead."""
        events = [
            self.create_event("Tomorrow event", days_offset=1),
            self.create_event("Next week", days_offset=7),
        ]
        today, week, two_week = filter_events(events, reference_time=self.get_base_time())
        assert len(today) == 1
        assert today[0]["summary"] == "Tomorrow event"
        assert len(week) == 1
        assert week[0]["summary"] == "Next week"
        assert len(two_week) == 0
    
    def test_filter_events_one_week(self):
        """Should filter events for 1 week ahead."""
        events = [
            self.create_event("Tomorrow", days_offset=1),
            self.create_event("One week", days_offset=7),
            self.create_event("Two weeks", days_offset=14),
        ]
        today, week, two_week = filter_events(events, reference_time=self.get_base_time())
        assert len(today) == 1
        assert len(week) == 1
        assert week[0]["summary"] == "One week"
        assert len(two_week) == 1
    
    def test_filter_events_two_weeks(self):
        """Should filter events for 2 weeks ahead."""
        events = [
            self.create_event("Two weeks", days_offset=14),
        ]
        today, week, two_week = filter_events(events, reference_time=self.get_base_time())
        assert len(today) == 0
        assert len(week) == 0
        assert len(two_week) == 1
        assert two_week[0]["summary"] == "Two weeks"
    
    def test_filter_events_ignores_past(self):
        """Should not include past events."""
        events = [
            self.create_event("Yesterday", days_offset=-1),
            self.create_event("Last week", days_offset=-7),
        ]
        today, week, two_week = filter_events(events, reference_time=self.get_base_time())
        assert len(today) == 0
        assert len(week) == 0
        assert len(two_week) == 0
    
    def test_filter_events_ignores_other_dates(self):
        """Should not include events on other specific dates."""
        events = [
            self.create_event("In 2 days", days_offset=2),
            self.create_event("In 5 days", days_offset=5),
            self.create_event("In 10 days", days_offset=10),
        ]
        today, week, two_week = filter_events(events, reference_time=self.get_base_time())
        assert len(today) == 0
        assert len(week) == 0
        assert len(two_week) == 0
    
    def test_filter_events_multiple_same_day(self):
        """Should include multiple events on the same target day."""
        events = [
            self.create_event("Event 1 tomorrow", days_offset=1, hours_offset=0),
            self.create_event("Event 2 tomorrow", days_offset=1, hours_offset=5),
        ]
        today, week, two_week = filter_events(events, reference_time=self.get_base_time())
        assert len(today) == 2
        assert len(week) == 0
        assert len(two_week) == 0


class TestEnvironmentValidation:
    """Test that required environment variables are documented."""
    
    def test_required_vars_in_env_example(self):
        """Verify .env.example has all required vars."""
        env_example_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            ".env.example"
        )
        with open(env_example_path) as f:
            content = f.read()
        
        required = ["GOOGLE_API_KEY", "CALENDAR_ID", "TELEGRAM_BOT_TOKEN", "TELEGRAM_GROUP_ID"]
        for var in required:
            assert var in content, f"{var} missing from .env.example"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
