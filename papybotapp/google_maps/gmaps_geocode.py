import os
import logging

import googlemaps


def get_address_coordinates(address: str):
    """"""
    gmaps = googlemaps.Client(key=os.getenv("API_KEY_FRONT"))

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
