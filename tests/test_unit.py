from typer.testing import CliRunner

from cli import app

runner = CliRunner()

def test_app():
    result = runner.invoke(app, ["test"])
    assert result.exit_code == 0
    assert "Testing" in result.stdout

def test_get_command_no_number_specified():
    result = runner.invoke(app, ["get"])
    assert result.exit_code == 0
    assert "IET Work" in result.stdout

def test_get_command_5_specified():
    result = runner.invoke(app, ["get", "5"])
    assert result.exit_code == 0
    assert "IET Work" in result.stdout

def test_create_command_with_arguments_not_recurring():
    result = runner.invoke(app, ["create", "--summary", "Test", "--isrecurring", "n", "--date", "2025-01-06", "--start", "08:00", "--end", "12:00", "--color", "Lavendar", "--confirm", "y"])
    assert result.exit_code == 0
    assert "Creating an event" in result.stdout
    assert "Event created" in result.stdout

def test_create_command_with_arguments_recurring_one_day():
    result = runner.invoke(app, ["create", "--summary", "Test", "--isrecurring", "y", "--days", "Monday", "--enddate", "2025-01-06", "--date", "2024-01-08", "--start", "09:45", "--end", "16:10", "--color", "Banana", "--confirm", "y"])
    assert result.exit_code == 0
    assert "Creating an event" in result.stdout
    assert "Event created" in result.stdout

def test_create_command_with_arguments_recurring_multiple_days():
    result = runner.invoke(app, ["create", "--summary", "Test", "--isrecurring", "y", "--days", "Monday, Wednesday, Friday", "--enddate", "2025-01-06", "--date", "2024-01-08", "--start", "12:00", "--end", "14:00", "--color", "Basil", "--confirm", "y"])
    assert result.exit_code == 0
    assert "Creating an event" in result.stdout
    assert "Event created" in result.stdout

def test_create_command_with_arguments_recurring_multiple_days():
    result = runner.invoke(app, ["create", "--summary", "Test", "--isrecurring", "y", "--days", "Everyday", "--enddate", "2025-01-06", "--date", "2024-01-08", "--start", "08:00", "--end", "12:00", "--color", "Graphite", "--confirm", "y"])
    assert result.exit_code == 0
    assert "Creating an event" in result.stdout
    assert "Event created" in result.stdout

def test_create_command_with_arguments_recurring_days_no_confirm():
    result = runner.invoke(app, ["create", "--summary", "Test", "--isrecurring", "y", "--days", "Tuesday, Thursday", "--enddate", "2025-01-06", "--date", "2024-01-08", "--start", "07:15", "--end", "11:30", "--color", "Tomato", "--confirm", "n"])
    assert result.exit_code == 0
    assert "Event creation cancelled" in result.stdout