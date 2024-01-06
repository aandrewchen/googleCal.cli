import os

import typer
from typing_extensions import Annotated

import inquirer

from InquirerPy import prompt as promptpy

from utils.auth import get_auth
from utils.get_event import get_upcoming_events, convert_time, convert_date
from utils.create_event import create_event

from googleapiclient.errors import HttpError

calendar_id = os.environ.get("CALENDAR_ID")

app = typer.Typer()

@app.command()
def create(
    summary: Annotated[str, typer.Option(help="What is the event?")] = None,
    isRecurring: Annotated[str, typer.Option(help="Is the event recurring? (y/n)")] = None,
    days: Annotated[str, typer.Option(help="If recurring, what days does this event occur? ['day', 'day', 'etc.']")] = None,
    endDate: Annotated[str, typer.Option(help="If recurring, when does this recurring event end? (YYYY-MM-DD)")] = None,
    date: Annotated[str, typer.Option(help="What date is the (first) event? (YYYY-MM-DD)")] = None,
    start: Annotated[str, typer.Option(help="What time does this event start? (HH:MM)")] = None,
    end: Annotated[str, typer.Option(help="What time does this event end? (HH:MM)")] = None,
    color: Annotated[str, typer.Option(help="What color should this event be?")] = None,
    confirm: Annotated[str, typer.Option(help="Are you sure you want to create this event? (y/n)")] = None,
):
    """
    Create an upcoming event with specified properties
    """
    if summary is None:
        summary = typer.prompt("What are you doing?")

    if isRecurring is None:
        isRecurring = typer.prompt("Is this a recurring event? (y/n)")

    if isRecurring == "y":
        if days is None:
            days = [
                inquirer.Checkbox('days',
                    message="Which days does this event occur?",
                    choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Everyday'],
                    carousel=True,
                ),
            ]

            days = inquirer.prompt(days)
        else:

            days = {
                "days": [day.strip() for day in days.split(',')],
            }

        if endDate is None:
            endDate = typer.prompt("When does this recurring event end? (YYYY-MM-DD)").replace("-", "")
        else:
            endDate = endDate.replace("-", "")

    if date is None:
        if isRecurring == "y":
            date = typer.prompt("What date is the first event? (YYYY-MM-DD)")
        else:
            date = typer.prompt("What date is the event? (YYYY-MM-DD)")

    if start is None:
        start = typer.prompt("What time does this event start? (HH:MM)")
    if end is None:
        end = typer.prompt("What time does this event end? (HH:MM)")

    startTime = f"{date}T{start}:00"
    endTime = f"{date}T{end}:00"

    if color is None:
        color = [
            {
                "type": "fuzzy",
                "message": "What color should this event be?",
                "choices": ['Lavendar', 'Sage', 'Grape', 'Flamingo', 'Banana', 'Tangerine', 'Peacock', 'Graphite', 'Blueberry', 'Basil', 'Tomato'],
                "name": "color",
            }
        ]

        color = promptpy(color)
        color = color["color"]

    date = convert_date(start)
    converted_start = convert_time(start)
    converted_end = convert_time(end)

    if confirm is None:
        confirm = typer.prompt("Are you sure you want to create this event? (y/n) (" + converted_start + ' to ' + converted_end + ", " + date + " | " + summary + ")")

    if confirm == "n":
        print("Event creation cancelled")
        return
    else:
        print("Creating an event")
        create_event(
            calendar_id, 
            summary if summary is None else summary, 
            color, 
            startTime, 
            endTime,
            isRecurring if isRecurring is None else isRecurring,
            days["days"] if isRecurring == "y" else None,
            endDate if isRecurring == "y" else None,
        )

@app.command()
def get(count: Annotated[str, typer.Argument()] = "1"):
    """
    Get the specified number of upcoming events. If no number is specified, gets the next event.
    """
    if count == '1':
        print("Getting the next event in your calendar")
    else:
        print(f"Getting the upcoming {count} events in your calendar")
    events = get_upcoming_events(calendar_id, count)
    if not events:
        print("No upcoming events found.")
    else:
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            date = convert_date(start)
            converted_start = convert_time(start)
            converted_end = convert_time(end)
            print(converted_start + ' to ' + converted_end + ", " + date + " | " + event["summary"])

@app.command()
def list_id(count: Annotated[str, typer.Argument()] = "1"):
    """
    List the ID's of the specified number of upcoming events. If no number is specified, gets the next event.
    """
    if count == '1':
        print("Getting the next event's ID in your calendar")
    else:
        print(f"Getting the upcoming {count} events' ID's in your calendar")
    events = get_upcoming_events(calendar_id, count)
    if not events:
        print("No upcoming events found.")
    else:
        for event in events:
            print("ID: " + event["id"] + " | " + event["summary"])

@app.command()
def delete(id: str):
    """
    Delete an event with the specified ID.
    """
    service = get_auth()
    try:
        event = service.events().get(calendarId=calendar_id, eventId=id).execute()
        
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        date = convert_date(start)
        converted_start = convert_time(start)
        converted_end = convert_time(end)

        confirm = typer.prompt("Are you sure you want to delete this event? (y/n) (" + converted_start + ' to ' + converted_end + ", " + date + " | " + event["summary"] + ")")

        if confirm == "n":
            print("Event deletion cancelled")
            return
        else:
            print("Deleting event")
            service.events().delete(calendarId=calendar_id, eventId=id).execute()
            print("Event deleted")
    except HttpError:
        print("No event found with specified ID")

@app.command()
def test():
    print("Testing")

if __name__ == "__main__":
    app()