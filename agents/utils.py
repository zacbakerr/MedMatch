import googlemaps
from typing import Tuple
import os

class DistanceCalculator:
    def __init__(self):
        self.gmaps = googlemaps.Client(key='AIzaSyAtAgnJbt2c7QX72BFsM4kluy7Z0AA-jAo')
    
    def calculate_travel_time(self, origin: str, destination: str) -> Tuple[int, float]:
        """
        Calculate travel time between two addresses using Google Distance Matrix API
        
        Args:
            origin: Patient's address
            destination: Facility's address
            
        Returns:
            Tuple[int, float]: (travel_time_minutes, distance_km)
        """
        try:
            result = self.gmaps.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode="driving",
                units="metric"
            )
            
            if result['rows'][0]['elements'][0]['status'] == 'OK':
                duration_seconds = result['rows'][0]['elements'][0]['duration']['value']
                distance_meters = result['rows'][0]['elements'][0]['distance']['value']
                
                return (duration_seconds // 60, distance_meters / 1000)
            else:
                return (None, None)
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return (None, None)

def calculate_distance_decay(travel_time_minutes: int, max_acceptable_time: int = 120) -> float:
    """
    Calculate decay factor based on travel time
    
    Args:
        travel_time_minutes: Time to reach facility in minutes
        max_acceptable_time: Maximum acceptable travel time in minutes
        
    Returns:
        float: Decay factor between 0 and 1
    """
    if travel_time_minutes is None:
        return 1.0
    
    if travel_time_minutes <= max_acceptable_time:
        # Linear decay up to max_acceptable_time
        return 1 - (travel_time_minutes / max_acceptable_time)
    else:
        return 0.0 
