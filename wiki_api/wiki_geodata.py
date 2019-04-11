import requests
import logging
from pprint import *

from google_maps.gmaps_geocode import get_address_coordinates
from input_parser.string_parser import clean


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

logging.basicConfig(level=logging.DEBUG)


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
        return

    try:
        page_id = response.json()['query']['geosearch'][0]['pageid']
    except KeyError:
        return

    logging.debug(f'Article id returned : {page_id}')
    return page_id


def get_article_content(page_id):
    """
    Wikipedia's page content from a page id
    :param page_id: Wikipedia's page id
    :return: Wikipedia's article content
    """

    params = {
        'action': 'query',
        'prop': 'revisions',
        'rvprop': 'content',
        'format': 'json',
        'formatversion': 2,
        'pageids': page_id
    }

    response = requests.get(API_URL, params=params)

    if not response.status_code == 200:
        logging.warning(f'Error when retrieving article content : {response.status_code}')
        return ""

    try:
        article_content = response.json()['query']['pages'][0]['revisions'][0]['content']
    except KeyError:
        return ""

    return article_content


def main(example):
    """
    Take the user input from the website, clean it with string_parser.py, get the coordinates with gmaps_geocode.py,
    get the Wikipedia's page id relative to the coordinates and get the article content of this page.
    :param example: user input entered in the website
    :return: Wikipedia's article content relative to the address +- SEARCH_RADIUS
    """
    address_user_input = clean(example)

    address_lat, address_lng = get_address_coordinates(address_user_input)

    if (address_lat, address_lng) == (0, 0):
        return

    page_id = get_page_id(address_lat, address_lng)
    article_content = get_article_content(page_id)

    return article_content

    # TODO: bool si article trouvé -> random Bot response based on bool
    # TODO: return dict/list coords, url, content, Bot response -> json


if __name__ == '__main__':
    # pprint(main(examples[-1]), width=200)
    get_article_content("test")
    # get_page_id("string", "string")
    # address_lat, address_lng = 46.8077191, 7.159642
    # r = session.get(API_URL.format(address_lat, address_lng)).json()
    #
    # print(page_id)

    # TODO: fullurl à la fin, changer params prop : info|extracts
    #  explaintext = ""
    #  inprop = url -> article url -> 'fullurl'
    #  exchars = exsentences = 1/10
