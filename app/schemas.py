from typing import List, Optional
from pydantic import BaseModel, Field

class ArticleResponse(BaseModel):
    id: str
    content: str
    title: str
    url: str
    source_name: str
    author: Optional[str] = None
    published_at: Optional[str] = None

class FetchNewsRequest(BaseModel):
    query: Optional[str] = Field(None, description="Search query")
    country: Optional[str] = Field("us", description="Country code")
    category: Optional[str] = Field("sports", description="News category (e.g., business, entertainment, sports, technology)")
    page_size: Optional[int] = Field(10,ge=1,le=20, description="Number of articles to fetch")
    page: Optional[int] = Field(1,ge=1, description="Page number for pagination")
    
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    top_k: int = Field(5, ge=1, le=20, description="Number of top relevant articles to retrieve(1-20)")

class QuestionRequest(BaseModel):
    question: str = Field(..., description="Question to ask!")
    top_k: int = Field(5, ge=1, le=20, description="Number of top relevant articles to consider for answering the question(1-20)")

class SearchResult(BaseModel):
    """Single search result"""
    id: str
    title: str
    source_name: str
    url: str
    similarity_score: float
    content_preview: str

class SearchResponse(BaseModel):
    """Response for search"""
    query: str
    results: List[SearchResult]
    total_results: int

class SourceInfo(BaseModel):
    """Source information"""
    title: str
    url: str
    source_name: str

class QuestionResponse(BaseModel):
    """Response for question answering"""
    question: str
    answer: str
    sources: List[SourceInfo]

class StatsResponse(BaseModel):
    """Database statistics"""
    total_articles_in_rag: int
    total_articles_in_vectordb: int
