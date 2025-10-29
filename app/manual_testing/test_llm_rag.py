import sys
sys.path.append("../../")

from app.services.news_fetcher import NewsFetcher
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService

fetcher = NewsFetcher()
rag = RAGService()
llm_service = LLMService()

## check database status
stats =rag.get_status()
print(f"Total articles in the collection: {stats['total_documents']}")

## if empty then fetch some articles and add to the database
if stats['total_documents'] ==0:
    print("No articles found in the collection. Fetching and adding articles...")
    ai_articles = fetcher.search_everything(query='artificial intelligence',page_size=10,sort_by='relevancy')
    sports_articles = fetcher.search_everything(query='sports',page_size=10,sort_by='relevancy')
    climate_articles = fetcher.search_everything(query='climate change',page_size=10,sort_by='relevancy')

    all_articles = ai_articles+sports_articles+climate_articles

    rag.add_articles(all_articles)
    stats =rag.get_status()
    print(f"Total articles in the collection after adding: {stats['total_documents']}")

questions = [
    "What are the latest advancements in artificial intelligence?",
    "How is climate change impacting global weather patterns?",
    "What are the recent highlights in the world of sports?"
]

for question in questions:
    response = llm_service.ask_question(question=question, top_k=2)
    print(f"Question: {response['question']}")
    print(f"Answer: {response['answer']}")
    print("Sources:")
    for source in response['sources']:
        print(f"- {source['title']} ({source['url']})")
    print("#" * 80)