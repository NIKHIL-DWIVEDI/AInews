import chromadb
import chromadb.config
import langchain
import os
from sentence_transformers import SentenceTransformer

from app.models import Article

class RAGService:
    def __init__(self,db_path="../data/chroma_db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.client = chromadb.PersistentClient(path=db_path,settings=chromadb.config.Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name="rag_collection",metadata={"description": "News artickles with embeddings"})
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("Embedding model initialized successfully.")

    def add_articles(self,articles: list[Article]) -> None:
        if not articles:
            print("No articles to add.")
            return
        
        count=0
        for article in articles:
            existing =  self.collection.get(ids=[article.id])
            if existing['ids']:
                print(f"Article with ID {article.id} already exists in the collection.")
                continue

            full_text = article.get_full_text()
            embedding = self.embedding_model.encode(full_text).tolist()
            self.collection.add(
                ids=[article.id],
                documents=[full_text],
                embeddings=[embedding],
                metadatas=[{
                    "title": article.title,
                    "url": article.url,
                    "source_name": article.source_name,
                    "published_at": article.published_at,
                }]
            )
            count+=1
        
        print(f"The total number of articles added in chromadb: {count}")
        return
    
    def search_articles(self,query,top_k=5) -> list[dict]:
        query_embeddings = self.embedding_model.encode(query).tolist()
        results = self.collection.query(query_embeddings=[query_embeddings],n_results=top_k)
        formatted_results = []
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i]
            similarity_score = 1/(1+distance)
            formatted_results.append({
                "id": results['ids'][0][i],
                "content": results['documents'][0][i],
                "metadata":results['metadatas'][0][i],
                "title": results['metadatas'][0][i].get("title",""),
                "url": results['metadatas'][0][i].get("url",""),
                "source_name": results['metadatas'][0][i].get("source_name",""),
                "similarity_score": similarity_score
            })

        print(f"The total number of results: {len(formatted_results)}")
        return formatted_results

    def get_status(self):
        return{
            "total_documents": self.collection.count(),
            "top 3 elements in collection": self.collection.peek(3)
        }

    def clear_storage(self):
        self.client.delete_collection("rag_collection")
        self.collection = self.client.get_or_create_collection(name="rag_collection",metadata={"description": "News artickles with embeddings"})
        print("Storage cleared !!")

