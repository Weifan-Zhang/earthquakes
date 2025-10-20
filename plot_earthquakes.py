from datetime import date
import matplotlib.pyplot as plt
import requests
import json
import numpy as np


def get_data():
    """Retrieve the data we will be working with."""
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"
        }
    )
    # parse JSON text into Python dictionary
    data = response.json()
    return data


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # Time is in milliseconds since epoch, so divide by 1000 to convert to seconds
    year = date.fromtimestamp(timestamp / 1000).year
    return year


def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_per_year = {}
    for eq in earthquakes:
        year = get_year(eq)
        mag = get_magnitude(eq)
        # Ignore None magnitudes (sometimes missing)
        if mag is not None:
            magnitudes_per_year.setdefault(year, []).append(mag)
    return magnitudes_per_year


def plot_number_per_year(earthquakes):
    """Plot the frequency (number) of earthquakes per year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())
    counts = [len(magnitudes_per_year[y]) for y in years]

    plt.figure(figsize=(10, 5))
    plt.plot(years, counts, marker='o', color='royalblue')
    plt.title("Number of Earthquakes per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("number_per_year.png")


def plot_average_magnitude_per_year(earthquakes):
    """Plot the average magnitude of earthquakes per year."""
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_per_year.keys())
    avg_mags = [np.mean(magnitudes_per_year[y]) for y in years]

    plt.figure(figsize=(10, 5))
    plt.plot(years, avg_mags, marker='o', color='darkorange')
    plt.title("Average Magnitude of Earthquakes per Year")
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("avg_magnitude_per_year.png")


if __name__ == "__main__":
    # Get the data we will work with
    quakes = get_data()['features']

    # Plot results
    plot_number_per_year(quakes)
    plot_average_magnitude_per_year(quakes)
    plt.show()