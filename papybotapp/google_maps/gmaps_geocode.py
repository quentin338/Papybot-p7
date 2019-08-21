import os
import logging

import googlemaps


def get_address_coordinates(address: str) -> dict:
    """
    Uses Geocode Google API to get the coordinates and formal address from a str input.

    :param address: The address you want the coordinates of.
    :return: a dict consisting of : latitude, longitude and formatted address (e.g. 32 Python's Street etc)

    """
    gmaps = googlemaps.Client(key=os.getenv("API_KEY_BACK"))

    try:
        geocode_result = gmaps.geocode(address)[0]
    except (IndexError, googlemaps.exceptions.HTTPError):
        logging.warning('Google Maps has no response for this address.')
        return {}

    address_lat = geocode_result['geometry']['location']['lat']
    address_lng = geocode_result['geometry']['location']['lng']
    address_formatted = geocode_result['formatted_address']

    address_clean = {
        "lat": address_lat,
        "lng": address_lng,
        "format": address_formatted
    }

    return address_clean


if __name__ == '__main__':
    pass
