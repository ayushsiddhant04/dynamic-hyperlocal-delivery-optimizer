import math
from typing import List, Tuple

import requests

from app.core.config import settings
from app.models.schemas import Location


def haversine_distance_km(loc1: Location, loc2: Location) -> float:
    """
    Computes the great-circle distance between two points on the Earth's surface
    using the Haversine formula.

    Returns:
        Distance in kilometers.
    """
    R = 6371.0

    lat1_rad = math.radians(loc1.latitude)
    lon1_rad = math.radians(loc1.longitude)
    lat2_rad = math.radians(loc2.latitude)
    lon2_rad = math.radians(loc2.longitude)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        math.sin(dlat / 2.0) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(dlon / 2.0) ** 2
    )

    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return round(R * c, 3)


def estimate_travel_time_minutes(
    distance_km: float,
    average_speed_kmh: float = 30.0,
) -> float:
    """
    Estimates travel time in minutes from a distance and average speed.

    This remains available for offline/test scenarios.
    """
    if average_speed_kmh <= 0:
        return 0.0

    hours = distance_km / average_speed_kmh

    return round(hours * 60.0, 1)


def compute_distance_matrix(locations: List[Location]) -> List[List[float]]:
    """
    Builds an N x N road-distance matrix using Mapbox Matrix API.

    Matrix values are returned in kilometers.

    Raises:
        ValueError: If Mapbox configuration is missing or the API fails.
    """
    if len(locations) < 2:
        return [[0.0] * len(locations) for _ in locations]

    if not settings.MAPBOX_ACCESS_TOKEN:
        raise ValueError("MAPBOX_ACCESS_TOKEN is not configured.")

    coordinates = ";".join(
        f"{location.longitude},{location.latitude}"
        for location in locations
    )

    url = (
        "https://api.mapbox.com/directions-matrix/v1/"
        f"mapbox/driving/{coordinates}"
    )

    params = {
        "annotations": "distance,duration",
        "access_token": settings.MAPBOX_ACCESS_TOKEN,
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise ValueError(
            "Unable to retrieve road distance matrix from Mapbox."
        ) from exc

    if data.get("code") != "Ok":
        raise ValueError(
            f"Mapbox Matrix API error: {data.get('message', data.get('code'))}"
        )

    distances = data.get("distances")

    if distances is None:
        raise ValueError("Mapbox Matrix API returned no distance matrix.")

    matrix: List[List[float]] = []

    for row in distances:
        converted_row = []

        for distance_meters in row:
            if distance_meters is None:
                raise ValueError(
                    "No drivable route exists between at least two locations."
                )

            converted_row.append(round(distance_meters / 1000.0, 3))

        matrix.append(converted_row)

    return matrix


def compute_travel_time_matrix(
    locations: List[Location],
) -> List[List[float]]:
    """
    Builds an N x N road-travel-time matrix using Mapbox Matrix API.

    Matrix values are returned in minutes.
    """
    if len(locations) < 2:
        return [[0.0] * len(locations) for _ in locations]

    if not settings.MAPBOX_ACCESS_TOKEN:
        raise ValueError("MAPBOX_ACCESS_TOKEN is not configured.")

    coordinates = ";".join(
        f"{location.longitude},{location.latitude}"
        for location in locations
    )

    url = (
        "https://api.mapbox.com/directions-matrix/v1/"
        f"mapbox/driving/{coordinates}"
    )

    params = {
        "annotations": "duration",
        "access_token": settings.MAPBOX_ACCESS_TOKEN,
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise ValueError(
            "Unable to retrieve road travel-time matrix from Mapbox."
        ) from exc

    if data.get("code") != "Ok":
        raise ValueError(
            f"Mapbox Matrix API error: {data.get('message', data.get('code'))}"
        )

    durations = data.get("durations")

    if durations is None:
        raise ValueError("Mapbox Matrix API returned no duration matrix.")

    matrix: List[List[float]] = []

    for row in durations:
        converted_row = []

        for duration_seconds in row:
            if duration_seconds is None:
                raise ValueError(
                    "No travel-time route exists between at least two locations."
                )

            converted_row.append(round(duration_seconds / 60.0, 1))

        matrix.append(converted_row)

    return matrix