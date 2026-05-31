# Python Weather App

A simple weather app that runs in the terminal. It tells you the current weather and forecast for any city.

## How to run

First install the library we need:

```
pip install requests
```

Then run it like this:

```
python weather.py London
python weather.py "New York"
python weather.py Tokyo --days 3
python weather.py "Buenos Aires" --units imperial
```

## What it shows

- Temperature and feels like temperature
- Humidity percentage
- Air pressure
- Wind speed and direction
- Cloud cover
- Sunrise and sunset times
- Multi day forecast (up to 7 days)

## Arguments

| What to type | What it does |
|-------------|-------------|
| city name | The city you want weather for (use quotes if its more than one word) |
| --days N | Shows forecast for N days (1 to 7) |
| --units metric | Temperature in Celsius (default) |
| --units imperial | Temperature in Fahrenheit |

## Examples

```
python weather.py London

London, GB
==========
Overcast
Temp:     16.9C  (feels 15.1C)
Humidity: 66%
Pressure: 1016 hPa
Wind:     13.7 km/h W
Clouds:   100%
Sunrise:  04:50
Sunset:   21:07
```

```
python weather.py "New York" --units imperial --days 3

New York, US
============
Clear
Temp:     48.2F  (feels 44.8F)
Humidity: 82%
Pressure: 1019 hPa
Wind:     4.1 mph NW
Clouds:   0%
Sunrise:  05:27
Sunset:   20:20

New York, US - 3-Day Forecast

Sun 31 May
     Overcast
     46.0F / 75.2F

Mon 01 Jun
     Overcast
     58.3F / 72.0F

Tue 02 Jun
     Overcast
     52.5F / 70.5F
```

## API used

This uses Open-Meteo which is free and doesnt need any API key or signup.

## Made with

- Python
- requests library
- Open-Meteo API
