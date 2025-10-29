import sys
sys.path.append("../../")

from app.services.news_fetcher import NewsFetcher

fetcher = NewsFetcher()

articles = fetcher.fetch_news(country="us", category="sports", page_size=5, page=1)
for article in articles:
    print(f"The article ID: {article.id}")
    print(f"Title: {article.title}")
    print(f"Description: {article.description}")
    print(f"Content: {article.content}")
    print(f"URL: {article.url}")
    full_text = article.get_full_text()
    print(f"Full Text: {full_text}")
    print("-" * 80)

print("#" * 80)
print("Fetch all news")

all_articles = fetcher.search_everything(query="sports",page_size=5,sort_by='relevancy')
for article in all_articles:
    print(f"The article ID: {article.id}")
    print(f"Title: {article.title}")
    print(f"Description: {article.description}")
    print(f"Content: {article.content}")
    print(f"URL: {article.url}")
    full_text = article.get_full_text()
    print(f"Full Text: {full_text}")    
    print("-" * 80)
