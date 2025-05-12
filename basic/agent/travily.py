from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(max_results=1)

print(search.invoke({"query": "今天北京天气怎么样？"}))
