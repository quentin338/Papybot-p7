import pytest

from wiki_api.wiki_geodata import get_page_id, get_article_content


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

        assert get_page_id(10, 10) is None

    def test_page_id_string_input(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                pass

            def json(self):
                return {"error": "invalid-coord"}

        mock_requests = MockRequestsGet
        mock_requests.status_code = 200

        monkeypatch.setattr('requests.get', mock_requests)

        assert get_page_id("string", "string") is None

    # get_article_content()
    def test_get_article_content_code_ok(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                pass

            def json(self):
                return {
                    'query': {
                        'pages': [{
                            'revisions': [{
                                'content': "Wiki content !"
                            }]
                        }]
                    }
                }

        mock_requests = MockRequestsGet
        mock_requests.status_code = 200

        monkeypatch.setattr('requests.get', mock_requests)

        assert get_article_content(120) == "Wiki content !"

    def test_get_article_content_code_not_ok(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                pass

            def json(self):
                return {'error': 404}

        mock_requests = MockRequestsGet
        mock_requests.status_code = 404

        monkeypatch.setattr('requests.get', mock_requests)

        assert get_article_content(120) == ""

    def test_get_article_content_key_error(self, monkeypatch):
        class MockRequestsGet:
            def __init__(self, url, params):
                pass

            def json(self):
                return {'error': 'KeyError'}

        mock_requests = MockRequestsGet
        mock_requests.status_code = 200

        monkeypatch.setattr('requests.get', mock_requests)

        assert get_article_content("string") == ""
