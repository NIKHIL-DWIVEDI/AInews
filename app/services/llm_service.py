
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app import config
from app.services import rag_service
from langchain_core.output_parsers import StrOutputParser


class LLMService:
    def __init__(self):
        self.llm = ChatGroq(
            model=config.Config().model,
            api_key=config.Config().groq_api_key,
            temperature=config.Config().temperature,
            max_tokens=config.Config().llm_max_tokens,
        )

        self.prompt_template = ChatPromptTemplate.from_template("""
        You are a helpful assistant that provides a summary of the news articles. Answer the question based on the context below.
        Context from news articles:
        {context}
        Question: {question}
        Instructions:
        1. Answer based primarily on the provided context
        2. Cite the sources by mentioning article titles or sources
        3. If the context doesn't contain enough information, say so
        4. Be concise but informative
        5. Use bullet points if listing multiple points
        Answer:                                                             
        """)

    def ask_question(self, question: str, top_k =5) -> dict:
        print("The question asked by the user: ", question)
        search_results = rag_service.RAGService().search_articles(query=question, top_k=top_k)

        if not search_results:
            return{
                "question": question,
                "answer": "No relevant articles found to answer the question.",
                "sources": []
            }
        
        context_parts = []
        for i, result in enumerate(search_results):
            context_parts.append(f"Article {i+1} Title: {result['title']}\nContent: {result['content']}\nSource: {result['source_name']}\nURL: {result['url']}\n")
        context = "\n".join(context_parts)

        chain = self.prompt_template | self.llm | StrOutputParser()

        response = chain.invoke({
            "context": context,
            "question": question
        })

        sources = []
        for result in search_results[:3]:
            sources.append({
                "title": result['title'],
                "url": result['url'],
                "source_name": result['source_name']
            })  
        return{
            "question": question,
            "answer": response,
            "sources": sources
        }

