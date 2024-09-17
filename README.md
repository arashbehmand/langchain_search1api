# LangChain Search1API Tools

This package provides LangChain tools for the [Search1API](https://www.search1api.com/) service, allowing easy integration of web search, news search, and web crawling capabilities into your LangChain applications.


**Disclaimer:** The author of this package is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Search1API, or any of its subsidiaries or its affiliates. The official Search1API website can be found at [https://www.search1api.com/](https://www.search1api.com/).


## Installation

You can install the package using pip:

```
pip install langchain_search1api
```

## Usage

Here's an example of how to use the tools in a LangChain application:

```python
from langchain_search1api import SearchTool, NewsTool, CrawlTool
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

# Initialize the tools
api_key = "your_api_key_here"
search_tool = SearchTool(api_key=api_key)
news_tool = NewsTool(api_key=api_key)
crawl_tool = CrawlTool(api_key=api_key)

# Initialize the language model
llm = OpenAI(temperature=0)

# Create the agent
agent = initialize_agent(
    tools=[search_tool, news_tool, crawl_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use the agent
result = agent.run("Search for recent news about artificial intelligence and summarize the top 3 results.")
print(result)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.