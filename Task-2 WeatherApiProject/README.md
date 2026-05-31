# Python API Integration Project

This project is designed for the **Python Developer Internship Task 2: API Integration**.

## Objective
Fetch weather data from a public API, parse the JSON response, display results cleanly, and let the user search and filter the output.

## Features
- Uses the `requests` module
- Searches a city by name
- Parses JSON response
- Displays current weather and a 7-day forecast
- Adds a filter for temperature or precipitation probability
- Logs all operations to `logs/operations.log`

## API Used
This project uses the Open-Meteo public weather API and geocoding API.

## Folder Structure
- `main.py` - complete script
- `requirements.txt` - dependency list
- `sample_input_output.txt` - sample run format
- `logs/operations.log` - runtime log file

## How to Run
1. Install Python 3.x
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python main.py
   ```

## Sample Input
- City name: `Hyderabad`
- Filter choice: `2`
- Minimum temperature: `30`

## Output
The script prints:
- matched locations
- selected location
- current weather
- filtered 7-day forecast

## Submission Notes
For internship submission, include:
- GitHub source code link
- Screenshots of output
- Separate document for this task
