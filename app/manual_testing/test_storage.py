import sys
sys.path.append("../../")

from app.services.news_fetcher import NewsFetcher
from app.services.storage import ArticleStorage

fetcher = NewsFetcher()
storage = ArticleStorage(storage_path="../data/storage.json")

## fetch some articles
articles = fetcher.fetch_news(country="us", category="sports", page_size=5, page=1)
print(f"Fetched {len(articles)} articles")

# save the articles
storage.write_articles(articles)
storage.get_stats()

## read the articles
# storage._read_articles()
# storage._get_stats()
# ## clear the storage
# storage._clear_storage()
# storage._get_stats()

all_articles = fetcher.search_everything(query="sports",page_size=5,sort_by='relevancy')
storage.write_articles(all_articles)
storage.get_stats()

