from typing import Optional
import requests
import sys
sys.path.append("../")
from app.config import Config
from app.models import Article

class NewsFetcher:
    DEFAULT_QUERY = "top headlines"
    
    def __init__(self):
        config = Config()
        self.api_key = config.news_api_key
        self.base_url = config.news_base_url
        self.everything_url = config.news_everything_url

    def fetch_news(self,
                   query: Optional[str]=DEFAULT_QUERY,
                   country="us",
                   category="sports",
                   page_size=5,
                   page=1) -> list[Article]:

        # NewsAPI /top-headlines endpoint doesn't support 'q' parameter with country/category
        # If query is provided and not default, use /everything endpoint instead
        if query and query != self.DEFAULT_QUERY:
            # Use /everything endpoint for keyword search
            url = self.everything_url
            params = {
                "apiKey": self.api_key,
                "q": query,
                "pageSize": page_size,
                "page": page,
                "sortBy": "relevancy"
            }
        else:
            # Use /top-headlines endpoint for country/category filtering
            url = self.base_url
            params = {
                "apiKey": self.api_key,
                "country": country,
                "category": category,
                "pageSize": page_size,
                "page": page
            }
            
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if response.status_code == 200:
                articles = data.get("articles", [])
                return self.parse_articles(articles)
            else:
                raise Exception(f"API call failed with status code: {response.status_code}, Response: {data}")
        except requests.RequestException as e:
            raise Exception(f"An error occurred while fetching news: {e}")
        
    def parse_articles(self, articles_data) -> list[Article]:
        articles = []
        for article_data in articles_data:
            title = article_data.get("title", "")
            description = article_data.get("description", "")
            content = article_data.get("content", "")
            url = article_data.get("url", "")
            source_name = article_data.get("source", {}).get("name", "")
            published_at = article_data.get("publishedAt", "")
            author = article_data.get("author", "")
            article = Article(
                title=title,
                description=description,
                content=content,
                url=url,
                source_name=source_name,
                published_at=published_at,
                author=author
            )
            articles.append(article)
        return articles
    
    def search_everything(self,query,page_size=20,sort_by='relevancy'):
        params = {
            "apiKey": self.api_key,
            "q": query,
            "pageSize": page_size,
            "sortBy": sort_by
        }
        try:
            response = requests.get(self.everything_url, params=params)
            data = response.json()
            if response.status_code == 200:
                articles = data.get("articles", [])
                return self.parse_articles(articles)
            else:
                raise Exception(f"API call failed with status code: {response.status_code}, Response: {data}")
        except requests.RequestException as e:
            raise Exception(f"An error occurred while fetching news: {e}")

