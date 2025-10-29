import sys
sys.path.append("../../")

## intialise
from app.services.news_fetcher import NewsFetcher
from app.services.rag_service import RAGService


fetcher = NewsFetcher()
rag = RAGService()

## fetch some articles
ai_articles = fetcher.search_everything(query='artificial intelligence',page_size=10,sort_by='relevancy')
sports_articles = fetcher.search_everything(query='sports',page_size=10,sort_by='relevancy')
climate_articles = fetcher.search_everything(query='climate change',page_size=10,sort_by='relevancy')

all_articles = ai_articles+sports_articles+climate_articles

## add articles
rag.add_articles(all_articles)
stats =rag.get_status()
print(f"Total articles in the collection: {stats['total_documents']}")
print(f"Top 3 elements in the collection: {stats['top 3 elements in collection']}")
## test the query 
results = rag.search_articles(query='what is the risk of AI?',top_k=3)
for i,result in enumerate(results):
    print(f"{result['title']}")
    print(f"similarity score : {result['similarity_score']}")
