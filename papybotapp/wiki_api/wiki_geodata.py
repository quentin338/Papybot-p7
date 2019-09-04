import requests
import logging
import random
from typing import Union
import pprint as pp

from papybotapp.google_maps import get_address_coordinates
from papybotapp.input_parser.string_parser import clean
from papybotapp.papybot_answers import PAPYBOT_GOOD_ANSWERS, PAPYBOT_BAD_ANSWERS


API_URL = "https://fr.wikipedia.org/w/api.php"
SEARCH_RADIUS = 10000  # In meters. Radius around the given point

logging.basicConfig(level=logging.WARNING)


def get_page_id(address_lat: Union[int, float], address_lng: Union[int, float]) -> int:
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


def get_article_infos(page_id: int) -> dict:
    """
    Wikipedia's page infos from a page id.

    :param page_id: Wikipedia's page id
    :return: Wikipedia's article url/content/thumbnail

    """
    params = {
        'action': 'query',
        'prop': 'info|extracts|pageimages',
        'inprop': 'url',
        'explaintext': '',
        'exintro': 1,
        'exsectionformat': 'plain',
        'format': 'json',
        'formatversion': 2,
        'pageids': page_id,
        'pithumbsize': 500
    }

    response = requests.get(API_URL, params=params)
    if not response.status_code == 200:
        logging.warning(f'Error when retrieving article content : {response.status_code}')
        return {}

    response = response.json()

    try:
        article_content = response['query']['pages'][0]['extract']
        article_full_url = response['query']['pages'][0]['fullurl']
        article_thumbnail = response['query']['pages'][0]['thumbnail']['source']

        article_infos = {
            'url': article_full_url,
            'content': article_content,
            'thumbnail': article_thumbnail
        }

        return article_infos

    except KeyError:
        return {}


def main_func(user_input: str) -> dict:
    """
    Uses custom parser to clean user_input, Geocode API to find coordinates of it, look for a page on wikipedia
    to find an article related to these coords and get first block of content of it.

    :param user_input: the question/address entered by the user.
    :return: dict containing: coordinates, address, wiki page url, wiki content and bot random sentence.

    """
    article_json = {
        'address': None,
        'coords': None,
        'url': None,
        'content': None,
        'thumbnail': None,
        'bot_response': random.choice(PAPYBOT_BAD_ANSWERS)
    }

    # We clean the input first
    address_user_input = clean(user_input)

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

        # We put Wikipedia's logo if there's no thumbnail on the article's page
        article_json['thumbnail'] = article_infos.get('thumbnail', "/static/img/wiki_logo.jpg")

        # All steps have been completed successfully, we change the "bad" answer to "good"
        # We add the address found in the answer for a more dynamic response
        if not any(article_json) is None:
            article_json['bot_response'] = random.choice(PAPYBOT_GOOD_ANSWERS).format(article_json['address'])

    except KeyError as e:
        logging.debug(e)

    return article_json


if __name__ == '__main__':
    # pprint(main_func(examples[4]), width=200)
    infos = get_article_infos(465230)
    pp.pprint(infos)
