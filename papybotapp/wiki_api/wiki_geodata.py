import requests
import logging
import random
from pprint import *

from papybotapp.google_maps import get_address_coordinates
from papybotapp.input_parser.string_parser import clean
from papybotapp.papybot_answers import PAPYBOT_GOOD_ANSWERS, PAPYBOT_BAD_ANSWERS


API_URL = "https://fr.wikipedia.org/w/api.php"
SEARCH_RADIUS = 10000  # In meters. Radius around the given point

examples = ["Salut ! Je ne sais pas vous mais je veux tout connaître du Stade de France à Paris !",
            "1, avenue du Général Leclerc à Bordeaux",
            "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms à Paris ?",
            "Bonjour je veux savoir l'adresse du 13 rue des Bisounours à Paris, merci Papybot.",
            "Salut grandpy! Comment s'est passé ta soirée avec Madame Pahud hier soir? Au fait, pendant que j'y pense,"
            " pourrais-tu m'indiquer où se trouve le musée d'art et d'histoire de Fribourg, s'il te plaît ?",
            "le 12 rue du Pigeon, tu connais ?", "où se situe l'adresse du Magasin de chaussures "
            "à Pouet-les-Bains ?", "où est la rue chaudron 54 ?", "Tour Eiffel", "Pessac-sur-dordogne"]

logging.basicConfig(level=logging.WARNING)


def get_page_id(address_lat, address_lng):
    """
    Converts coordinates into a Wikipedia's page id relative to the place
    :param address_lat: latitude of a place
    :param address_lng: longitude of a place
    :return: Wikipedia's page id. Link to an article referring to the place around SEARCH_RADIUS of it
    """

    params = {
        'action': 'query',
        'list': 'geosearch',
        'gsradius': SEARCH_RADIUS,
        'gscoord': f'{address_lat}|{address_lng}',
        'format': 'json',
        'formatversion': 2
    }

    response = requests.get(API_URL, params=params)

    if not response.status_code == 200:
        logging.warning(f'Error when retrieving WIKI article ID : {response.status_code}')
        return 0

    try:
        page_id = response.json()['query']['geosearch'][0]['pageid']
    except KeyError:
        return 0

    logging.debug(f'Article id returned : {page_id}')
    return page_id


def get_article_infos(page_id):
    """
    Wikipedia's page content from a page id
    :param page_id: Wikipedia's page id
    :return: Wikipedia's article content
    """

    params = {
        'action': 'query',
        'prop': 'info|extracts',
        'inprop': 'url',
        'explaintext': '',
        'exintro': 1,
        'exsectionformat': 'plain',
        'format': 'json',
        'formatversion': 2,
        'pageids': page_id
    }

    response = requests.get(API_URL, params=params)

    if not response.status_code == 200:
        logging.warning(f'Error when retrieving article content : {response.status_code}')
        return {}

    response = response.json()

    try:
        article_content = response['query']['pages'][0]['extract']
        article_full_url = response['query']['pages'][0]['fullurl']

        article_infos = {
            'url': article_full_url,
            'content': article_content
        }

        return article_infos

    except KeyError:
        return {}


def main_func(example):
    """    """
    article_json = {
        'address': None,
        'coords': None,
        'url': None,
        'content': None,
        'bot_response': random.choice(PAPYBOT_BAD_ANSWERS)
    }

    # We clean the input first
    address_user_input = clean(example)

    # Block try/except to catch any problem at any step (GoogleMaps not finding the place, Wiki not having any
    # related page...
    try:
        address_coords = get_address_coordinates(address_user_input)

        article_json['coords'] = (address_coords['lat'], address_coords['lng'])
        article_json['address'] = address_coords['format']

        page_id = get_page_id(address_coords['lat'], address_coords['lng'])
        article_infos = get_article_infos(page_id)

        article_json['url'] = article_infos['url']
        article_json['content'] = article_infos['content']

        if not any(article_json) is None:
            article_json['bot_response'] = random.choice(PAPYBOT_GOOD_ANSWERS)

    except KeyError as e:
        logging.debug(e)

    return article_json


if __name__ == '__main__':
    pprint(main_func(examples[4]), width=200)

