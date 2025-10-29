from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ArticleResponse, FetchNewsRequest, QuestionRequest, QuestionResponse, StatsResponse
from app.services.llm_service import LLMService
from app.services.news_fetcher import NewsFetcher
from app.services.rag_service import RAGService
from app.services.storage import ArticleStorage

app = FastAPI(title="AI News Research Assistant",description="An application that leverages LLMs and RAG to provide answers based on the latest news articles.",version="1.0.0")

## add cors middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    ## print the exact object received
    print(f"Type of request received: {type(request)}")
    print(f"request country: {request.country}")
    print(f"request query: {request.query}")
    print(f"request category: {request.category}")
    print(f"request page_size: {request.page_size}")
    print(f"request page: {request.page}")
    print("Fetching news...")

    articles =news_fetcher.fetch_news(query=request.query, country=request.country, category=request.category, page_size=request.page_size,page=request.page)
    print("length of articles fetched:",len(articles))
    if not articles:
        print("No articles fetched from the news API.")
        raise HTTPException(status_code=404, detail="No articles found for the given parameters.")
    
    ## save to storage 
    storage.write_articles(articles)
    ## save to vector db
    rag_service.add_articles(articles)

    ## convert to response model
    response_articles = [ArticleResponse(**article.to_dict()) for article in articles]
    return response_articles

@app.post("/search")
def search_articles():
    pass

@app.post("/ask",response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        result = llm_service.ask_question(question=request.question,top_k=request.top_k)
        return QuestionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/articles",response_model=list[ArticleResponse])
def get_all_articles(limit: int =10):
    try:
        # read all the articles from storage
        articles = storage.read_articles()
        ## limti the articles
        articles = articles[:limit]
        response = [ArticleResponse(**article.to_dict()) for article in articles]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/clear")
def clear_all_data():
    pass


