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


def compute_road_matrices(
    locations: List[Location],
) -> Tuple[List[List[float]], List[List[float]]]:
    """
    Builds road-distance and road-travel-time matrices using one
    Mapbox Matrix API request.

    Returns:
        Tuple containing:
        - distance matrix in kilometers
        - duration matrix in minutes
    """
    if len(locations) < 2:
        empty_matrix = [[0.0] * len(locations) for _ in locations]
        return empty_matrix, empty_matrix

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
            "Unable to retrieve road distance and travel-time data from Mapbox."
        ) from exc

    if data.get("code") != "Ok":
        raise ValueError(
            f"Mapbox Matrix API error: {data.get('message', data.get('code'))}"
        )

    distances = data.get("distances")
    durations = data.get("durations")

    if distances is None:
        raise ValueError("Mapbox Matrix API returned no distance matrix.")

    if durations is None:
        raise ValueError("Mapbox Matrix API returned no duration matrix.")

    distance_matrix: List[List[float]] = []
    duration_matrix: List[List[float]] = []

    for distance_row, duration_row in zip(distances, durations):
        distance_values: List[float] = []
        duration_values: List[float] = []

        for distance_meters, duration_seconds in zip(
            distance_row,
            duration_row,
        ):
            if distance_meters is None:
                raise ValueError(
                    "No drivable route exists between at least two locations."
                )

            if duration_seconds is None:
                raise ValueError(
                    "No travel time exists between at least two locations."
                )

            distance_values.append(
                round(distance_meters / 1000.0, 3)
            )

            duration_values.append(
                round(duration_seconds / 60.0, 1)
            )

        distance_matrix.append(distance_values)
        duration_matrix.append(duration_values)

    return distance_matrix, duration_matrix


def compute_distance_matrix(
    locations: List[Location],
) -> List[List[float]]:
    """
    Builds an N x N road-distance matrix in kilometers.

    Uses Mapbox road distances.
    """
    distance_matrix, _ = compute_road_matrices(locations)
    return distance_matrix


def compute_travel_time_matrix(
    locations: List[Location],
) -> List[List[float]]:
    """
    Builds an N x N road-travel-time matrix in minutes.

    Uses Mapbox road travel durations.
    """
    _, duration_matrix = compute_road_matrices(locations)
    return duration_matrix