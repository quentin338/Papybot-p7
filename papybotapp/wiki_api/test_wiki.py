from papybotapp.wiki_api.wiki_geodata import get_page_id, get_article_infos


class TestWikiApi:
    # get_page_id()
    def test_get_page_id_code_ok(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                pass

            def json(self):
                return {
                    'query': {
                        'geosearch': [{
                            'pageid': 1337
                        }]
                    }
                }

        mock_requests = MockRequestsGet
        mock_requests.status_code = 200

        monkeypatch.setattr('requests.get', mock_requests)

        assert get_page_id(10, 10) == 1337

    def test_page_id_code_not_ok(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                pass

            def json(self):
                return {
                    'query': {
                        'geosearch': [{
                            'pageid': 1337
                        }]
                    }
                }

        mock_requests = MockRequestsGet
        mock_requests.status_code = 404

        monkeypatch.setattr('requests.get', mock_requests)

        assert get_page_id(10, 10) == 0

    def test_page_id_string_input(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                pass

            def json(self):
                return {"error": "invalid-coord"}

        mock_requests = MockRequestsGet
        mock_requests.status_code = 200

        monkeypatch.setattr('requests.get', mock_requests)

        assert get_page_id("string", "string") == 0

    # get_article_infos()
    def test_get_article_infos_code_ok(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                self.status_code = 200

            def json(self):
                return {
                    'query': {
                        'pages': [{
                                'extract': 'Wiki content !',
                                'fullurl': 'https://www.python.org',
                                'thumbnail': {
                                    'source': 'https://mythumbnail.com'
                                }
                            }]
                    }
                }

        monkeypatch.setattr('requests.get', MockRequestsGet)

        assert get_article_infos(120) == {
            'url': 'https://www.python.org',
            'content': 'Wiki content !',
            'thumbnail': 'https://mythumbnail.com'
        }

    def test_get_article_infos_code_not_ok(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                self.status_code = 404

        monkeypatch.setattr('requests.get', MockRequestsGet)

        assert get_article_infos(120) == {}

    def test_get_article_infos_key_error(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                pass

            def json(self):
                return {}

        mock_requests = MockRequestsGet
        mock_requests.status_code = 200

        monkeypatch.setattr('requests.get', mock_requests)

        assert get_article_infos(120) == {}
