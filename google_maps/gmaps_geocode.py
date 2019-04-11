import logging

import googlemaps

API_KEY = "AIzaSyBMKnBfvBZdbejSYcP0uvMzhC2cKSkXcvc"
address_user_input = "Openclassrooms"


def get_address_coordinates(address: str):
    """
    Converts an address (str) in coordinates
    :param address: str: user input from the website, cleaned by string_parser.py
    :return: tuples of coordinates (latitude, longitude) of the address found by Google API
    """
    gmaps = googlemaps.Client(key=API_KEY)

    try:
        geocode_result = gmaps.geocode(address)[0]
        address_lat = geocode_result['geometry']['location']['lat']
        address_lng = geocode_result['geometry']['location']['lng']

        return address_lat, address_lng
    except IndexError:
        logging.warning('Google Maps has no response for this address.')
        return 0, 0


if __name__ == '__main__':
    print(get_address_coordinates(99999999))

    # TODO: récupérer l'adresse "clean" de la réponse /
