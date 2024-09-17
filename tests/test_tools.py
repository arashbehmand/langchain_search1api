"""Unit tests for langchain_search1api tools."""

import unittest
from unittest import TestCase
from unittest.mock import patch
from langchain_search1api import SearchTool, NewsTool, CrawlTool


class TestSearch1APITools(TestCase):
    """Unit tests for Search1API tools."""

    def setUp(self):
        self.api_key = "test_api_key"

    @patch("langchain_search1api.tools.requests.post")
    def test_search_tool(self, mock_post):
        mock_post.return_value.json.return_value = {
            "results": [{"title": "Test Result"}]
        }
        mock_post.return_value.raise_for_status.return_value = None

        tool = SearchTool(api_key=self.api_key)
        result = tool.run("test query")

        self.assertIn("Test Result", result)

    @patch("langchain_search1api.tools.requests.post")
    def test_news_tool(self, mock_post):
        mock_post.return_value.json.return_value = {"results": [{"title": "Test News"}]}
        mock_post.return_value.raise_for_status.return_value = None

        tool = NewsTool(api_key=self.api_key)
        result = tool.run("test query")

        self.assertIn("Test News", result)

    @patch("langchain_search1api.tools.requests.post")
    def test_crawl_tool(self, mock_post):
        mock_post.return_value.json.return_value = {"results": {"title": "Test Crawl"}}
        mock_post.return_value.raise_for_status.return_value = None

        tool = CrawlTool(api_key=self.api_key)
        result = tool.run("https://example.com")

        self.assertIn("Test Crawl", result)


if __name__ == "__main__":
    unittest.main()
