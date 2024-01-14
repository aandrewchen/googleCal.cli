# gcal.cli

gcal.cli is a command-line interface tool built with Python3, Pytest, Typer, and the Google Calendar API. It's designed to automate procedures and manage Google Calendar events.

## Features

- **Create, read, update, and delete** Google Calendar events 📅
- **List** upcoming events 🖊️
- **Support** for recurring events ✅
- **Display** events in a table format 📋
- **Start** a timer for a quick event ⏱️ 

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/aandrewchen/gcal.cli.git
cd gcal.cli
pip install -r requirements.txt
```

## Usage
You can use the `--help` flag with any command to get information about how to use it.
![Screenshot 2024-01-14 at 3 11 58 AM](https://github.com/aandrewchen/gcal.cli/assets/125727520/0369b174-f370-4634-8ba2-426b77185991)

### Here are some examples of how to use gcal.cli:

#### Get the next 3 events and display them in a table
```bash
python cli.py get 3 --table y
```
![Screenshot 2024-01-14 at 3 09 31 AM](https://github.com/aandrewchen/gcal.cli/assets/125727520/211789ec-b5a7-4c59-b4e8-650c653479f1)

#### Create a new event
```bash
python cli.py create
```

#### List ID of the next event in your calendar
*Optionally include count to get the specified number of upcoming events*
```bash
python cli.py list-id <count>
```

#### Delete an event by ID
*Replace required id with the ID of the event you want to delete*
```bash
python cli.py delete <id>
```
![Screenshot 2024-01-14 at 3 24 58 AM](https://github.com/aandrewchen/gcal.cli/assets/125727520/37438305-0044-4f4a-99c2-27bc9e41dabc)

#### Start a timer for a quick event
```bash
python cli.py start
```

#### Stop timer
```bash
python cli.py stop
```

## Testing
You can run the tests with Pytest:
```bash
pytest
```
To see test converage, run:
```bash
coverage run -m pytest
```

## Contributing
Contributions are welcome! Please create a new issue if you find a bug or have a feature request. If you want to contribute code, please fork the repository and create a pull request.
