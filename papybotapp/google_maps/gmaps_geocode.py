import logging

import googlemaps

from .CONSTANTS import GMAPS_API_KEY as API_KEY


def get_address_coordinates(address: str):
    """"""
    gmaps = googlemaps.Client(key=API_KEY)

    try:
        geocode_result = gmaps.geocode(address)[0]

        address_lat = geocode_result['geometry']['location']['lat']
        address_lng = geocode_result['geometry']['location']['lng']
        address_formatted = geocode_result['formatted_address']

        address_clean = {
            "lat": address_lat,
            "lng": address_lng,
            "format": address_formatted
        }

        return address_clean

    except IndexError:
        logging.warning('Google Maps has no response for this address.')
        return {}


if __name__ == '__main__':
    pass
