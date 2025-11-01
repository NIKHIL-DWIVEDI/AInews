import time 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.schemas import ArticleResponse, FetchNewsRequest, QuestionRequest, QuestionResponse, SearchRequest, SearchResponse, SearchResult, StatsResponse
from app.services.llm_service import LLMService
from app.services.news_fetcher import NewsFetcher
from app.services.rag_service import RAGService
from app.services.storage import ArticleStorage

from app.metrics import articles_fetched, articles_stored, llm_api_latency, rag_query_latency, rag_queries

app = FastAPI(title="AI News Research Assistant",description="An application that leverages LLMs and RAG to provide answers based on the latest news articles.",version="1.0.0")

## add cors middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## add prometheus instrumentation]
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=False,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True
)
instrumentator.instrument(app).expose(app,endpoint="/metrics")

## intialize services
news_fetcher = NewsFetcher()
storage = ArticleStorage(storage_path="../data/storage.json")
rag_service = RAGService()
llm_service = LLMService()

@app.get("/")
def root():
    return {"message": "Welcome to the AI News Research Assistant API!", "version": "1.0.0", "status": "running"}

@app.get("/stats",response_model=StatsResponse)
def get_status():
    rag_stas = rag_service.get_status()
    storage_stats = storage.get_stats()
    return{
        "total_articles_in_rag": rag_stas['total_documents'],
        "total_articles_in_vectordb": storage_stats
    }

@app.post("/fetch-news",response_model=list[ArticleResponse])
def fetch_news(request: FetchNewsRequest):
    articles =news_fetcher.fetch_news(query=request.query, country=request.country, category=request.category, page_size=request.page_size,page=request.page)
    print("length of articles fetched:",len(articles))
    if not articles:
        print("No articles fetched from the news API.")
        raise HTTPException(status_code=404, detail="No articles found for the given parameters.")
    
    articles_fetched.labels(source="newsapi",category=request.category).inc(len(articles))
    ## save to storage 
    saved_articles_len = storage.write_articles(articles)
    articles_stored.inc(saved_articles_len)
    ## save to vector db
    rag_service.add_articles(articles)

    ## convert to response model
    response_articles = [ArticleResponse(**article.to_dict()) for article in articles]
    return response_articles

@app.post("/search",response_model=SearchResponse)
def search_articles(request: SearchRequest):
    try:
        rag_queries.labels(query_type='search').inc(1)
        start_time = time.time()
        results = rag_service.search_articles(query=request.query,top_k=request.top_k)
        end_time = time.time()
        duration = end_time - start_time
        rag_query_latency.labels(query_type='search').observe(duration)
        formatted_results = [
            SearchResult(
                id=r['id'],
                title=r['title'],
                source_name=r['source_name'],
                url=r['url'],
                similarity_score=r['similarity_score'],
                content_preview=r['content'][:200] + "..."
            )
            for r in results
        ]
        
        return SearchResponse(
            query=request.query,
            results=formatted_results,
            total_results=len(formatted_results)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask",response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        start_time = time.time()
        result = llm_service.ask_question(question=request.question,top_k=request.top_k)
        end_time = time.time()
        duration = end_time - start_time
        rag_query_latency.labels(query_type='qa').observe(duration)
        return QuestionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/articles",response_model=list[ArticleResponse])
def get_all_articles(limit: int =10):
    try:
        articles = storage.read_articles()
        articles = articles[:limit]
        response = [ArticleResponse(**article.to_dict()) for article in articles]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/clear")
def clear_all_data():
    try:
        storage.clear_storage()
        rag_service.clear_storage()
        print("Cleared all data from storage and vector DB.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



