import json
import unittest

from ytelegraph.api import TelegraphAPI


class FakeAccount:
    access_token = "token"
    author_name = "Anonymous"
    author_url = None


def make_api() -> TelegraphAPI:
    api = TelegraphAPI.__new__(TelegraphAPI)
    api.account = FakeAccount()
    api.base_url = "https://api.telegra.ph"
    api.request_timeout = 10.0
    return api


class TelegraphAPITests(unittest.TestCase):
    def test_extract_path_accepts_paths_and_telegraph_urls(self) -> None:
        api = make_api()

        self.assertEqual(api._extract_path("Sample-Page-12-15"), "Sample-Page-12-15")
        self.assertEqual(
            api._extract_path("https://telegra.ph/Sample-Page-12-15/"),
            "Sample-Page-12-15",
        )

    def test_extract_path_rejects_unknown_urls(self) -> None:
        api = make_api()

        with self.assertRaises(ValueError):
            api._extract_path("https://example.com/Sample-Page-12-15")

    def test_create_page_sends_json_content(self) -> None:
        api = make_api()
        calls = []

        def fake_request(method, endpoint, data):
            calls.append((method, endpoint, data))
            return {"url": "https://telegra.ph/Sample-Page-12-15"}

        api._make_request = fake_request
        url = api.create_page("Title", [{"tag": "p", "children": ["Hello"]}])

        self.assertEqual(url, "https://telegra.ph/Sample-Page-12-15")
        method, endpoint, data = calls[0]
        self.assertEqual((method, endpoint), ("POST", "createPage"))
        self.assertEqual(json.loads(data["content"]), [{"tag": "p", "children": ["Hello"]}])
        self.assertEqual(data["access_token"], "token")

    def test_get_page_preserves_page_fields(self) -> None:
        api = make_api()

        def fake_request(method, endpoint, data):
            self.assertEqual((method, endpoint), ("GET", "getPage"))
            return {
                "path": "Sample-Page-12-15",
                "url": "https://telegra.ph/Sample-Page-12-15",
                "title": "Title",
                "description": "Description",
                "views": 7,
                "content": [{"tag": "p", "children": ["Hello"]}],
            }

        api._make_request = fake_request

        page = api.get_page("Sample-Page-12-15")

        self.assertTrue(page["success"])
        self.assertEqual(page["path"], "Sample-Page-12-15")
        self.assertEqual(page["views"], 7)
        self.assertEqual(page["attempts"], 1)
        self.assertIsNone(page["error"])

    def test_delete_page_verifies_replaced_content(self) -> None:
        api = make_api()
        expected_content = [{"tag": "p", "children": ["This page has been deleted."]}]
        calls = []

        def fake_request(method, endpoint, data):
            calls.append((method, endpoint, data))
            return {"url": "https://telegra.ph/Sample-Page-12-15"}

        api._make_request = fake_request
        api.get_page = lambda path: {
            "success": True,
            "title": "404",
            "content": expected_content,
        }

        self.assertTrue(api.delete_page("Sample-Page-12-15"))
        self.assertEqual(calls[0][1], "editPage")


if __name__ == "__main__":
    unittest.main()
