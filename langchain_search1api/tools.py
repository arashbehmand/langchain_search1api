"""
This module provides tools for interacting with the Search1API service.
It includes classes for performing web searches, news searches, and web crawling.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Final, ClassVar
import json

from pydantic import BaseModel, Field
import requests
from langchain.tools import BaseTool

# Base URL for the API
BASE_URL = "https://api.search1api.com"

class SearchParameters(BaseModel):
    """Common parameters for search and news search operations."""
    query: str = Field(..., description="The query you want to ask")
    search_service: Optional[str] = Field(
        None,
        description="The search service you want to choose (google, bing, duckduckgo)"
    )
    max_results: Optional[int] = Field(
        5,
        description="The number of results you want to have (1-100)"
    )
    crawl_results: Optional[int] = Field(
        0,
        description="The number of results you want to crawl (0-10)"
    )
    image: Optional[bool] = Field(
        False,
        description="Search including image URLs"
    )
    gl: Optional[str] = Field(None, description="The country you want to search")
    hl: Optional[str] = Field(None, description="The language you want to search")

class CrawlParameters(BaseModel):
    """Parameters for crawling a specific webpage."""
    url: str = Field(..., description="The URL to crawl")

class Search1APITool(BaseTool, ABC):
    """Base class for Search1API tools."""
    name: str
    description: str
    api_key: str
    timeout: int = 40  # Default timeout value
    is_single_input: Final[bool] = True

    @abstractmethod
    def _run(self, query: str, *args: Any, ** kwargs: Any) -> str:
        """Abstract method to be implemented by subclasses."""

    def _make_request(self, endpoint: str, data: dict) -> dict:
        """Make a request to the Search1API service."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

class SearchTool(Search1APITool):
    """Tool for performing web searches using the search1api service."""
    name: str = "search1api_search"
    description: str = "Useful for performing web searches using the search1api service."

    def _run(self, query: str, *args: Any, **kwargs: Any) -> str:
        search_params = SearchParameters(query=query, ** kwargs)
        result = self._make_request("/search", search_params.model_dump(exclude_none=True))
        return json.dumps(result, indent=2)

class NewsTool(Search1APITool):
    """Tool for performing news searches using the search1api service."""
    name: str = "search1api_news"
    description: str = "Useful for performing news searches using the search1api service."

    def _run(self, query: str, *args: Any, **kwargs: Any) -> str:
        search_params = SearchParameters(query=query, ** kwargs)
        result = self._make_request("/news", search_params.model_dump(exclude_none=True))
        return json.dumps(result, indent=2)

class CrawlTool(Search1APITool):
    """Tool for crawling a specific webpage using the search1api service."""
    name: str = "search1api_crawl"
    description: str = "Useful for crawling a specific webpage using the search1api service."

    def _run(self, query: str, *args: Any, **kwargs: Any) -> str:
        crawl_params = CrawlParameters(url=query)
        result = self._make_request("/crawl", crawl_params.model_dump())
        return json.dumps(result, indent=2)
