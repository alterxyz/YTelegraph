import json
import os
import tempfile
import unittest
from unittest.mock import patch

from ytelegraph.account import TelegraphAccount


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self) -> None:
        pass

    def json(self):
        return self.payload


class TelegraphAccountTests(unittest.TestCase):
    def test_prefers_environment_token(self) -> None:
        with patch.dict(os.environ, {"TELEGRA_PH_TOKEN": "env-token"}):
            with patch.object(TelegraphAccount, "get_account_info", return_value={}):
                with patch.object(TelegraphAccount, "_get_token") as get_token:
                    with patch.object(TelegraphAccount, "_create_account") as create_account:
                        account = TelegraphAccount()

        self.assertEqual(account.access_token, "env-token")
        get_token.assert_not_called()
        create_account.assert_not_called()

    def test_get_account_info_serializes_fields_and_uses_timeout(self) -> None:
        account = TelegraphAccount.__new__(TelegraphAccount)
        account.base_url = "https://api.telegra.ph"
        account.access_token = "token"
        account.request_timeout = 3.0

        with patch("ytelegraph.account.requests.get") as mock_get:
            mock_get.return_value = FakeResponse(
                {"ok": True, "result": {"short_name": "Sandbox", "page_count": 1}}
            )

            result = account.get_account_info(["short_name", "page_count"])

        self.assertEqual(result["page_count"], 1)
        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs["timeout"], 3.0)
        self.assertEqual(json.loads(kwargs["params"]["fields"]), ["short_name", "page_count"])

    def test_save_token_uses_configured_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            token_path = os.path.join(temp_dir, "token.txt")
            account = TelegraphAccount.__new__(TelegraphAccount)

            with patch.dict(os.environ, {"PH_TOKEN_PATH": token_path}):
                account._save_token("secret-token")

            with open(token_path, "r", encoding="utf-8") as token_file:
                self.assertEqual(token_file.read(), "secret-token")


if __name__ == "__main__":
    unittest.main()
