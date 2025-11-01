from prometheus_client import Counter, Histogram, Gauge

articles_fetched = Counter(
    'articles_fetched',
    'Total number of articles fetched from the News API',
    ['source','category']
)

articles_stored = Counter(
    'articles_stored',
    'Total number of articles stored in the database'
)

rag_queries = Counter(
    'rag_queries_total',
    'Total number of RAG queries made',
    ['query_type']
)

llm_queries = Counter(
    'llm_queries_total',
    'Total number of LLM API calls made',
    ['model']
)

## track rag query latency
rag_query_latency = Histogram(
    'rag_query_latency_seconds',
    'Latency for RAG queries in seconds',
    ['query_type'],
    buckets=[0.1, 0.5, 1, 2.5, 5,]
)

## track llm api latency
llm_api_latency = Histogram(
    'llm_api_latency_seconds',
    'Latency for LLM API calls in seconds',
    ['model'],
    buckets=[0.5, 1, 2.5, 5, 10, 20]
)




