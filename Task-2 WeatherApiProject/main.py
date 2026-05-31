import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import requests


logging.basicConfig(
    filename="logs/operations.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


@dataclass
class Location:
    name: str
    country: str
    admin1: str
    latitude: float
    longitude: float
    timezone: str


WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def log_and_print(message: str) -> None:
    print(message)


def fetch_json(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    logging.info("Requesting %s with params=%s", url, params)
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, dict) and data.get("error"):
        raise ValueError(data.get("reason", "API returned an error"))
    return data


def geocode_city(city: str) -> List[Location]:
    data = fetch_json(GEOCODING_URL, {"name": city, "count": 5, "language": "en", "format": "json"})
    results = data.get("results", [])
    locations: List[Location] = []
    for item in results:
        locations.append(
            Location(
                name=item.get("name", "Unknown"),
                country=item.get("country", "Unknown"),
                admin1=item.get("admin1", ""),
                latitude=float(item["latitude"]),
                longitude=float(item["longitude"]),
                timezone=item.get("timezone", "auto"),
            )
        )
    return locations


def choose_location(locations: List[Location]) -> Location:
    if not locations:
        raise ValueError("No matching locations found.")
    if len(locations) == 1:
        return locations[0]

    print("\nMatching locations:")
    for idx, loc in enumerate(locations, start=1):
        extra = f", {loc.admin1}" if loc.admin1 else ""
        print(f"{idx}. {loc.name}{extra}, {loc.country}  ({loc.latitude:.4f}, {loc.longitude:.4f})")

    while True:
        choice = input("Select the correct location number: ").strip()
        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(locations):
                return locations[number - 1]
        print("Invalid choice. Please enter one of the listed numbers.")


def get_weather(location: Location) -> Dict[str, Any]:
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": "temperature_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "timezone": location.timezone,
        "forecast_days": 7,
    }
    return fetch_json(FORECAST_URL, params)


def weather_description(code: int) -> str:
    return WMO_CODES.get(code, "Unknown")


def print_current_weather(data: Dict[str, Any]) -> None:
    current = data.get("current", {})
    if not current:
        print("\nCurrent weather: not available")
        return

    code = int(current.get("weather_code", -1))
    print("\nCurrent weather")
    print("-" * 50)
    print(f"Time           : {current.get('time', 'N/A')}")
    print(f"Temperature    : {current.get('temperature_2m', 'N/A')} °C")
    print(f"Wind Speed     : {current.get('wind_speed_10m', 'N/A')} km/h")
    print(f"Condition      : {weather_description(code)} (code {code})")


def apply_filter(times: List[str], highs: List[float], lows: List[float], rain: List[float], codes: List[int]) -> List[Dict[str, Any]]:
    print("\nFilter options")
    print("1. Show all forecast days")
    print("2. Show days with maximum temperature above or equal to a value")
    print("3. Show days with precipitation probability above or equal to a value")
    choice = input("Enter filter choice (1/2/3): ").strip()

    threshold: Optional[float] = None
    if choice == "2":
        threshold = float(input("Enter minimum temperature in °C: ").strip())
    elif choice == "3":
        threshold = float(input("Enter minimum precipitation probability in %: ").strip())

    rows: List[Dict[str, Any]] = []
    for i, day in enumerate(times):
        row = {
            "date": day,
            "high": highs[i],
            "low": lows[i],
            "rain": rain[i],
            "code": codes[i],
            "description": weather_description(int(codes[i])),
        }
        if choice == "2" and threshold is not None and row["high"] < threshold:
            continue
        if choice == "3" and threshold is not None and row["rain"] < threshold:
            continue
        rows.append(row)
    return rows


def print_forecast(data: Dict[str, Any]) -> None:
    daily = data.get("daily", {})
    if not daily:
        print("\nForecast: not available")
        return

    times = daily.get("time", [])
    highs = daily.get("temperature_2m_max", [])
    lows = daily.get("temperature_2m_min", [])
    rain = daily.get("precipitation_probability_max", [])
    codes = daily.get("weather_code", [])

    filtered_rows = apply_filter(times, highs, lows, rain, codes)
    print("\n7-Day Forecast")
    print("-" * 80)
    if not filtered_rows:
        print("No days matched the selected filter.")
        return

    for row in filtered_rows:
        print(
            f"{row['date']} | High: {row['high']} °C | Low: {row['low']} °C | "
            f"Rain %: {row['rain']} | {row['description']} (code {row['code']})"
        )


def main() -> None:
    print("Python API Integration Project")
    print("=" * 35)

    try:
        city = input("Enter a city name to search weather for: ").strip()
        if not city:
            raise ValueError("City name cannot be empty.")

        logging.info("User searched city: %s", city)
        matches = geocode_city(city)
        location = choose_location(matches)

        print(
            f"\nSelected location: {location.name}, "
            f"{location.admin1 + ', ' if location.admin1 else ''}{location.country}"
        )

        weather_data = get_weather(location)
        print_current_weather(weather_data)
        print_forecast(weather_data)

        logging.info("Successfully completed search for %s", city)
        print("\nTask completed successfully.")

    except requests.exceptions.RequestException as exc:
        logging.exception("Network/API error")
        print(f"Network/API error: {exc}")
    except ValueError as exc:
        logging.exception("Validation/API error")
        print(f"Error: {exc}")
    except Exception as exc:
        logging.exception("Unexpected error")
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
