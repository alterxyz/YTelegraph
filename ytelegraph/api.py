import json
import re
import time
from typing import Optional, Dict, List, Any, Union

import requests
from requests.exceptions import RequestException

from .account import TelegraphAccount
from .md_to_dom import md_to_dom


class TelegraphAPI:
    """Interacts with the Telegraph API to manage pages and accounts.

    This class provides methods for:
      - Creating and managing Telegraph pages
      - Handling account-related operations

    Attributes:
        account: The Telegraph account associated with this API instance.
        base_url: The base URL for the Telegraph API.

    Note:
        Methods that accept content offer two options:

        1. Methods ending with '_md' for Markdown input.
        2. Regular methods for Telegraph DOM input.

        Choose the method that best fits your use case.
    """

    def __init__(
        self,
        access_token: Optional[str] = None,
        short_name: str = "Your Name",
        author_name: str = "Anonymous",
        author_url: Optional[str] = None,
    ) -> None:
        """Initializes a TelegraphAPI object.

        Args:
            access_token: The access token for the Telegraph account.
            short_name: The short name of the Telegraph account.
            author_name: The author name associated with the account.
            author_url: The author URL associated with the account.
        """
        self.account: TelegraphAccount = TelegraphAccount(
            access_token, short_name, author_name, author_url
        )
        self.base_url: str = "https://api.telegra.ph"

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Makes a request to the Telegraph API.

        Args:
            method: The HTTP method to use (GET or POST).
            endpoint: The API endpoint to call.
            data: The data to send with the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            RequestException: If there's an error with the request.
            Exception: If the API returns an error response.
        """
        url: str = f"{self.base_url}/{endpoint}"
        try:
            if method.upper() == "GET":
                response: requests.Response = requests.get(url, params=data)
            else:
                response: requests.Response = requests.post(url, data=data)
            response.raise_for_status()
            result = response.json()
            if not result.get("ok"):
                raise Exception(f"API error: {result.get('error', 'Unknown error')}")
            return result["result"]
        except RequestException as e:
            print(f"Error making request to {endpoint}: {e}")
            raise

    def _extract_path(self, path_or_url: str) -> str:
        """Extracts the path from a Telegraph URL or path string.

        Args:
            path_or_url: The Telegraph URL or path.

        Returns:
            str: The extracted path.

        Raises:
            ValueError: If the input is not a valid Telegraph path or URL.
        """
        match = re.search(
            r"(?:https?://(?:telegra\.ph/|telegraph\.com/))?([^/]+)/?$", path_or_url
        )
        if match:
            return match.group(1)
        raise ValueError("Invalid path or URL format")

    def create_page(
        self,
        title: str,
        content: List[Dict[str, Any]],
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        return_content: bool = False,
    ) -> str:
        """Creates a new Telegraph page with raw content.

        Args:
            title: The title of the page.
            content: The content of the page in Telegraph node format.
            author_name: The author name for this specific page.
            author_url: The author URL for this specific page.
            return_content: Whether to return the content in the response.

        Returns:
            str: The URL of the created page.

        Note:
            Use the `create_page_md` method for Markdown content.
        """
        data: Dict[str, Any] = {
            "access_token": self.account.access_token,
            "title": title,
            "content": json.dumps(content),
            "return_content": return_content,
            "author_name": author_name or self.account.author_name,
            "author_url": author_url or self.account.author_url,
        }
        result: Dict[str, Any] = self._make_request("POST", "createPage", data)
        if return_content:
            print("Returned content:", result.get("content"))
        return result["url"]

    def create_page_md(
        self,
        title: str,
        content: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        return_content: bool = False,
    ) -> str:
        """Creates a new Telegraph page with Markdown content.

        Args:
            title: The title of the page.
            content: The content of the page in Markdown format.
            author_name: The author name for this specific page.
            author_url: The author URL for this specific page.
            return_content: Whether to return the content in the response.

        Returns:
            str: The URL of the created page.
        """
        telegraph_content: List[Dict[str, Any]] = md_to_dom(content)
        return self.create_page(
            title, telegraph_content, author_name, author_url, return_content
        )

    def edit_page(
        self,
        path: str,
        content: List[Dict[str, Any]],
        title: Optional[str] = None,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        return_content: bool = False,
    ) -> str:
        """Edits an existing Telegraph page with raw content.

        If no title is provided, the original title of the page will be used.

        Args:
            path: The path or URL of the page to edit.
            content: The new content of the page in Telegraph node format.
            title: The new title of the page. If None, the original title is kept.
            author_name: The new author name for this specific page.
            author_url: The new author URL for this specific page.
            return_content: Whether to return the content in the response.

        Returns:
            str: The URL of the edited page.

        Note:
            Use the `edit_page_md` method for Markdown content.
        """
        path = self._extract_path(path)
        if not title:
            title = self.get_page(path)["title"]
        data: Dict[str, Any] = {
            "access_token": self.account.access_token,
            "path": path,
            "title": title,
            "content": json.dumps(content),
            "return_content": return_content,
            "author_name": author_name or self.account.author_name,
            "author_url": author_url or self.account.author_url,
        }
        result: Dict[str, Any] = self._make_request("POST", "editPage", data)
        return result["url"]

    def edit_page_md(
        self,
        path: str,
        content: str,
        title: Optional[str] = None,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        return_content: bool = False,
    ) -> str:
        """Edits an existing Telegraph page with Markdown content.

        If no title is provided, the original title of the page will be used.

        Args:
            path: The path or URL of the page to edit.
            content: The new content of the page in Markdown format.
            title: The new title of the page. If None, the original title is kept.
            author_name: The new author name for this specific page.
            author_url: The new author URL for this specific page.
            return_content: Whether to return the content in the response.

        Returns:
            str: The URL of the edited page.
        """
        telegraph_content: List[Dict[str, Any]] = md_to_dom(content)
        result = self.edit_page(
            path, telegraph_content, title, author_name, author_url, return_content
        )
        return result

    def edit_page_md_append_to_front(
        self,
        path: str,
        content: str,
        title: Optional[str] = None,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        return_content: bool = False,
    ) -> str:
        """Appends Markdown content to the front of an existing Telegraph page.

        Args:
            path: The path or URL of the page to edit.
            content: The Markdown content to append to the front of the page.
            title: The new title of the page. If None, the original title is kept.
            author_name: The new author name for this specific page.
            author_url: The new author URL for this specific page.
            return_content: Whether to return the content in the response.

        Returns:
            str: The URL of the edited page.
        """
        telegraph_content = md_to_dom(content) + self.get_page(path)["content"]
        result = self.edit_page(
            path, telegraph_content, title, author_name, author_url, return_content
        )
        return result

    def edit_page_md_append_to_back(
        self,
        path: str,
        content: str,
        title: Optional[str] = None,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        return_content: bool = False,
    ) -> str:
        """Appends Markdown content to the back of an existing Telegraph page.

        Args:
            path: The path or URL of the page to edit.
            content: The Markdown content to append to the back of the page.
            title: The new title of the page. If None, the original title is kept.
            author_name: The new author name for this specific page.
            author_url: The new author URL for this specific page.
            return_content: Whether to return the content in the response.

        Returns:
            str: The URL of the edited page.
        """
        original_content = self.get_page(path)["content"]
        telegraph_content: List[Dict[str, Any]] = original_content + md_to_dom(content)
        result = self.edit_page(
            path, telegraph_content, title, author_name, author_url, return_content
        )
        return result

    def delete_page(self, path: str) -> bool:
        """Deletes a Telegraph page.

        Replaces all page information with meaningless text.

        Args:
            path: The path or URL of the page to delete.

        Returns:
            bool: True if the page was successfully deleted, False otherwise.
        """
        path = self._extract_path(path)
        expected_content = [{"tag": "p", "children": ["This page has been deleted."]}]
        data: Dict[str, Any] = {
            "access_token": self.account.access_token,
            "path": path,
            "title": "404",
            "content": json.dumps(expected_content),
            "author_name": "Deleted",
            "author_url": None,
        }
        result: Dict[str, Any] = self._make_request("POST", "editPage", data)
        # Verify deletion by checking the latest content.
        latest_content = self.get_page(path)
        # Compare the content as lists of dictionaries
        return latest_content == expected_content

    def get_page(
        self,
        path: str,
        return_content: bool = True,
        retry: bool = True,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> Dict[str, Any]:
        """Retrieves a Telegraph page with retry mechanism and custom error content.

        Args:
            path: The path or URL of the page to retrieve.
            return_content: Whether to return the content in the response.
            retry: Whether to use the retry mechanism.
            max_retries: Maximum number of retry attempts if retry is True.
            retry_delay: Delay between retry attempts in seconds if retry is True.

        Returns:
            dict: A dictionary containing:
                - 'success': Boolean indicating if the operation was successful.
                - 'title': The title of the page (None if unsuccessful).
                - 'content': The content of the page or custom error content.
                - 'error': Original error message (if not successful).
                - 'attempts': Number of attempts made to retrieve the page.

        Note:
            If all retry attempts fail, a custom error content in Markdown format
            will be returned instead of the actual page content.
        """
        path = self._extract_path(path)
        data: Dict[str, Any] = {
            "path": path,
            "return_content": return_content,
        }

        result = {
            "success": False,
            "title": None,
            "content": [],
            "error": None,
            "attempts": 0,
        }

        for attempt in range(max_retries if retry else 1):
            result["attempts"] += 1
            try:
                api_result: Dict[str, Any] = self._make_request("GET", "getPage", data)
                result["success"] = True
                result["content"] = api_result.get("content", [])
                result["title"] = api_result.get("title")
                return result
            except Exception as e:
                result["error"] = str(e)
                if attempt < max_retries - 1 and retry:
                    time.sleep(retry_delay)
                else:
                    # Create custom error content
                    error_md = f"# Error\n\nFailed to retrieve page after {result['attempts']} attempts.\n\nError: {result['error']}"
                    result["content"] = md_to_dom(error_md)
                    return result

        return result

    def get_page_list(self, offset: int = 0, limit: int = 50) -> Dict[str, Any]:
        """Retrieves a list of pages belonging to the Telegraph account.

        Args:
            offset: The sequential number of the first page to be returned.
                Defaults to 0.
            limit: The number of pages to be returned.
                Defaults to 50, maximum is 200.

        Returns:
            dict: The list of pages and total count. For example:

            ```json
            {
              "total_count": 1,
              "pages": [
                {
                  "path": "Page-title-07-12-2",
                  "url": "https://telegra.ph/Page-title-07-12-2",
                  "title": "Page title",
                  "description": "This is page 1",
                  "views": 23,
                  "can_edit": True
                }
              ]
            }
            ```
        """
        data: Dict[str, Any] = {
            "access_token": self.account.access_token,
            "offset": offset,
            "limit": max(1, min(200, limit)),  # Ensure limit is between 1 and 200
        }
        return self._make_request("GET", "getPageList", data)

    def get_views(
        self,
        path: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
    ) -> Dict[str, int]:
        """Retrieves the number of views for a Telegraph article.

        Args:
            path: The path or URL of the article.
            year: The year to get views for.
            month: The month to get views for.
            day: The day to get views for.
            hour: The hour to get views for.

        Returns:
            dict: A dictionary containing the number of page views.
                For example: `{"views": 42}`

        Note:
            If a more precise date is provided, all less precise date
            arguments must also be provided. For example, if `day` is
            provided, both `year` and `month` must also be provided.
        """
        path = self._extract_path(path)
        data: Dict[str, Any] = {"path": path}
        if year:
            data["year"] = year
        if month and year:
            data["month"] = month
        if day and month and year:
            data["day"] = day
        if hour and day and month and year:
            data["hour"] = hour
        result: Dict[str, Any] = self._make_request("GET", "getViews", data)
        return {"views": result["views"]}

    def get_account_info(self, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Retrieves account information.

        Args:
            fields: List of account fields to return.

        Returns:
            dict: The account information. For example:

            ```json
            {
              "short_name": "Your Name",
              "author_name": "Anonymous",
              "author_url": "https://example.com",
              "auth_url": "https://edit.telegra.ph/auth/..."
            }
            ```
        """
        return self.account.get_account_info(fields)

    def revoke_access_token(self) -> bool:
        """Revokes the current access token and generates a new one.

        Returns:
            bool: True if the token was successfully revoked and a new one
                generated, False otherwise.
        """
        return self.account.revoke_access_token()

    def edit_account_info(
        self,
        short_name: Optional[str] = None,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> bool:
        """Edits the account information.

        Args:
            short_name: The new short name for the account.
            author_name: The new author name for the account.
            author_url: The new author URL for the account.

        Returns:
            bool: True if the account information was successfully updated,
                False otherwise.
        """
        return self.account.edit_account_info(short_name, author_name, author_url)

    def _md_to_dom(self, content: str) -> List[Dict[str, Any]]:
        """Converts Markdown content to Telegraph DOM format.

        This is an internal helper method and should not be called directly.

        Args:
            content: The content in Markdown format.

        Returns:
            list: The content in Telegraph DOM format.
        """
        return md_to_dom(content)
