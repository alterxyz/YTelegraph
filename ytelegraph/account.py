import json
import os
from pathlib import Path
from typing import Optional, Dict, List, Any

import requests
from requests.exceptions import RequestException


class TelegraphAccount:
    """Interacts with the Telegraph API to manage accounts.

    This class provides methods for:
      - Creating a new account
      - Getting account information
      - Revoking and generating new access tokens
      - Editing account information

    Attributes:
        TOKEN_FILENAME (str): The default filename for storing the access token.
        access_token (str): The access token for the Telegraph account.
        base_url (str): The base URL for the Telegraph API.
        short_name (str): The short name of the Telegraph account.
        author_name (str): The author name associated with the account.
        author_url (str): The author URL associated with the account.

    Example:
        >>> account = TelegraphAccount()
        >>> print(account.short_name)  # Output: Your Name
        >>> account.edit_account_info(author_name="New Author Name")
        >>> print(account.author_name)  # Output: New Author Name
    """

    TOKEN_FILENAME: str = "ph_token.txt"

    def __init__(
        self,
        access_token: Optional[str] = None,
        short_name: str = "Your Name",
        author_name: str = "Anonymous",
        author_url: Optional[str] = None,
    ) -> None:
        """Initializes a TelegraphAccount object.

        Args:
            access_token: The access token for the Telegraph account.
                If not provided, it will be loaded from the token file or a
                new account will be created.
            short_name: The short name of the Telegraph account.
                Only used when creating a new account. Defaults to "Your Name".
            author_name: The author name associated with the account.
                Only used when creating a new account. Defaults to "Anonymous".
            author_url: The author URL associated with the account.
                Only used when creating a new account. Defaults to None.
        """
        self.base_url: str = "https://api.telegra.ph"
        self.access_token: str = (
            access_token
            or self._get_token()
            or self._create_account(short_name, author_name, author_url)
        )
        account_info: Dict[str, Any] = self.get_account_info()
        self.short_name: str = account_info.get("short_name", short_name)
        self.author_name: str = account_info.get("author_name", author_name)
        self.author_url: Optional[str] = account_info.get("author_url", author_url)

    def _get_token_file_path(self) -> Path:
        """Gets the path to the access token file.

        The function checks for a custom token file path defined in the
        'PH_TOKEN_PATH' environment variable. If not found, it looks for the
        token file in the following locations in order:
            1. Current working directory: './ph_token.txt'
            2. User's home directory: '~/.ph_token'
            3. Current working directory: './ph_token.txt' (fallback)

        Returns:
            Path: The path to the access token file.
        """
        if "PH_TOKEN_PATH" in os.environ:
            return Path(os.environ["PH_TOKEN_PATH"])
        cwd_token: Path = Path.cwd() / self.TOKEN_FILENAME
        if cwd_token.exists():
            return cwd_token
        home: Path = Path.home()
        if home.exists():
            return home / ".ph_token"
        return Path.cwd() / self.TOKEN_FILENAME

    def _get_token(self) -> Optional[str]:
        """Gets the access token from the token file.

        Returns:
            str: The access token if found in the token file, otherwise None.
        """
        token_file: Path = self._get_token_file_path()
        if token_file.exists():
            with open(token_file, "r") as f:
                return f.read().strip()
        return None

    def _save_token(self, token: str) -> None:
        """Saves the access token to the token file.

        Args:
            token: The access token to save.
        """
        token_file: Path = self._get_token_file_path()
        token_file.parent.mkdir(parents=True, exist_ok=True)
        with open(token_file, "w") as f:
            f.write(token)

    def _delete_token(self) -> None:
        """Deletes the access token file."""
        token_file: Path = self._get_token_file_path()
        if token_file.exists():
            token_file.unlink()

    def _create_account(
        self, short_name: str, author_name: str, author_url: Optional[str]
    ) -> Optional[str]:
        """Creates a new Telegraph account.

        Args:
            short_name: The short name of the Telegraph account.
            author_name: The author name associated with the account.
            author_url: The author URL associated with the account.

        Returns:
            str: The access token of the newly created account if successful,
                otherwise None.
        """
        url: str = f"{self.base_url}/createAccount"
        data: Dict[str, Any] = {
            "short_name": short_name,
            "author_name": author_name,
            "author_url": author_url,
        }
        try:
            response: requests.Response = requests.post(url, data=data)
            response.raise_for_status()
            access_token: str = response.json()["result"]["access_token"]
            self._save_token(access_token)
            print(f"Account created with access token: {access_token}")
            return access_token
        except RequestException as e:
            print(f"Error creating account: {e}")
            return None

    def get_account_info(self, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Gets the account information for the current user.

        Args:
            fields: A list of fields to retrieve.
                If None, all fields are retrieved.

        Returns:
            dict: A dictionary containing the account information if
                successful, otherwise an empty dictionary.
        """
        url: str = f"{self.base_url}/getAccountInfo"
        params: Dict[str, Any] = {"access_token": self.access_token}
        if fields:
            params["fields"] = "[" + ",".join(f'"{field}"' for field in fields) + "]"
        try:
            response: requests.Response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()["result"]
        except RequestException as e:
            print(f"Error getting account info: {e}")
            return {}

    def get_authorization_url(self) -> str:
        """Gets the authorization URL for the current user.

        This URL allows the user to log in and grant access to the app.

        Returns:
            str: The authorization URL.
        """
        # we call the getAccountInfo with auth_url method to get the link
        return self.get_account_info(fields=["auth_url"]).get("auth_url", "")

    def revoke_access_token(self) -> bool:
        """Revokes the current access token and generates a new one.

        Returns:
            bool: True if the token was successfully revoked and a new one
                generated, otherwise False.
        """
        url: str = f"{self.base_url}/revokeAccessToken"
        data: Dict[str, str] = {"access_token": self.access_token}
        try:
            response: requests.Response = requests.post(url, data=data)
            response.raise_for_status()
            self._delete_token()
            new_token: str = response.json()["result"]["access_token"]
            self._save_token(new_token)
            self.access_token = new_token
            return True
        except RequestException as e:
            print(f"Error revoking access token: {e}")
            return False

    def edit_account_info(
        self,
        short_name: Optional[str] = None,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> bool:
        """Edits the account information for the current user.

        Args:
            short_name: The new short name for the account.
            author_name: The new author name for the account.
            author_url: The new author URL for the account.

        Returns:
            bool: True if the account information was successfully updated,
                otherwise False.
        """
        url: str = f"{self.base_url}/editAccountInfo"
        data: Dict[str, Any] = {"access_token": self.access_token}
        if short_name:
            data["short_name"] = short_name
        if author_name:
            data["author_name"] = author_name
        if author_url:
            data["author_url"] = author_url
        try:
            response: requests.Response = requests.post(url, data=data)
            response.raise_for_status()
            updated_info: Dict[str, Any] = response.json()["result"]
            self.short_name = updated_info.get("short_name", self.short_name)
            self.author_name = updated_info.get("author_name", self.author_name)
            self.author_url = updated_info.get("author_url", self.author_url)
            return True
        except RequestException as e:
            print(f"Error editing account info: {e}")
            return False
