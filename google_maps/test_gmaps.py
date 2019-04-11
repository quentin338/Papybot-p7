import pytest

from google_maps.gmaps_geocode import get_address_coordinates


def test_get_address_coordinates(monkeypatch):
    class MockGoogleMapsClient:
        def __init__(self, key):
            pass

        def geocode(self, address):
            return [{
                'geometry': {
                    'location': {
                             'lat': 100,
                             'lng': 200,
                         }
                }
            }]

    monkeypatch.setattr('googlemaps.Client', MockGoogleMapsClient)

    assert get_address_coordinates("test") == (100, 200)


def test_get_address_coordinates_index_error(monkeypatch):
    class MockGoogleMapsClient:
        def __init__(self, key):
            pass

        def geocode(self, address):
            return []

    monkeypatch.setattr('googlemaps.Client', MockGoogleMapsClient)

    assert get_address_coordinates('Invalid place') == (0, 0)
