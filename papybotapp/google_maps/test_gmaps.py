from papybotapp.google_maps import get_address_coordinates


def test_get_address_coordinates(monkeypatch):
    class MockGoogleMapsClient:
        def __init__(self, key):
            pass

        def geocode(self, address):
            return [{
                'formatted_address': "Clean address",
                'geometry': {
                    'location': {
                             'lat': 100,
                             'lng': 200,
                         }
                }
            }]

    monkeypatch.setattr('googlemaps.Client', MockGoogleMapsClient)

    assert get_address_coordinates("test") == {
                                                'format': "Clean address",
                                                'lat': 100,
                                                'lng': 200
                                            }


def test_get_address_coordinates_index_error(monkeypatch):
    class MockGoogleMapsClient:
        def __init__(self, key):
            pass

        def geocode(self, address):
            return []

    monkeypatch.setattr('googlemaps.Client', MockGoogleMapsClient)

    assert get_address_coordinates('Invalid place') == {}
