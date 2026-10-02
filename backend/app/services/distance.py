import math
from typing import List, Tuple
from app.models.schemas import Location


def haversine_distance_km(loc1: Location, loc2: Location) -> float:
    """
    Computes the great-circle distance between two points on the Earth's surface
    using the Haversine formula.

    Returns:
        Distance in kilometers.
    """
    R = 6371.0  # Earth's mean radius in kilometers

    lat1_rad = math.radians(loc1.latitude)
    lon1_rad = math.radians(loc1.longitude)
    lat2_rad = math.radians(loc2.latitude)
    lon2_rad = math.radians(loc2.longitude)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        math.sin(dlat / 2.0) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 3)


def estimate_travel_time_minutes(
    distance_km: float, average_speed_kmh: float = 30.0
) -> float:
    """
    Estimates travel time in minutes based on distance and average urban speed.

    Args:
        distance_km: Distance in km.
        average_speed_kmh: Urban speed (default 30 km/h for hyperlocal delivery).

    Returns:
        Estimated time in minutes.
    """
    if average_speed_kmh <= 0:
        return 0.0
    hours = distance_km / average_speed_kmh
    return round(hours * 60.0, 1)


def compute_distance_matrix(locations: List[Location]) -> List[List[float]]:
    """
    Builds an N x N symmetric distance matrix (in km) for a list of locations.
    """
    n = len(locations)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dist = haversine_distance_km(locations[i], locations[j])
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix
