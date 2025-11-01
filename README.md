# 🤖 AI News Research Assistant

An intelligent news research assistant powered by Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) that helps you stay informed with the latest news while providing intelligent answers to your questions.

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120.0-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Kubernetes Deployment](#-kubernetes-deployment)
- [Monitoring](#-monitoring)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **📰 News Fetching**: Retrieve the latest news articles from multiple categories and countries using NewsAPI
- **🔍 Semantic Search**: Find relevant articles using vector similarity search powered by ChromaDB
- **💬 AI-Powered Q&A**: Ask questions and get intelligent answers based on fetched news articles using Groq LLM
- **📊 Monitoring**: Built-in Prometheus metrics and Grafana dashboards for observability
- **🎨 Web Interface**: User-friendly frontend for interacting with the assistant
- **🐳 Docker Support**: Full containerization with Docker Compose
- **☸️ Kubernetes Ready**: Production-ready Kubernetes manifests
- **⚡ High Performance**: Async FastAPI backend for optimal performance

## 🏗 Architecture

The system follows a microservices architecture with the following components:

```
┌─────────────────┐
│   Frontend      │
│  (HTML/CSS/JS)  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐      ┌──────────────┐
│   FastAPI App   │─────→│   NewsAPI    │
│   (Backend)     │      └──────────────┘
└────────┬────────┘
         │
    ┌────┴─────┬─────────────┬──────────────┐
    ↓          ↓             ↓              ↓
┌────────┐ ┌────────┐  ┌──────────┐  ┌─────────┐
│ChromaDB│ │ Groq   │  │Prometheus│  │ Grafana │
│(Vector)│ │  LLM   │  │(Metrics) │  │(Dashbrd)│
└────────┘ └────────┘  └──────────┘  └─────────┘
```

**Components:**
- **FastAPI Backend**: RESTful API handling news fetching, search, and Q&A
- **NewsAPI**: External news source for fetching latest articles
- **ChromaDB**: Vector database for storing article embeddings
- **Sentence Transformers**: Generate embeddings for semantic search
- **Groq LLM**: Large language model for answering questions
- **Prometheus**: Metrics collection and monitoring
- **Grafana**: Metrics visualization and dashboards

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**
- **Docker** and **Docker Compose** (for containerized deployment)
- **Kubernetes** (optional, for K8s deployment)
- **Git**

### API Keys Required

You'll need to obtain the following API keys:

1. **NewsAPI Key**: Sign up at [newsapi.org](https://newsapi.org/)
2. **Groq API Key**: Sign up at [console.groq.com](https://console.groq.com/)

## 🚀 Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/NIKHIL-DWIVEDI/AInews.git
   cd AInews
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.development.example .env.development  # Create if doesn't exist
   ```
   
   Edit `.env.development` and add your API keys:
   ```env
   NEWS_API_KEY=your_newsapi_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

6. **Access the application**
   - API: http://localhost:8001
   - API Docs: http://localhost:8001/docs
   - Frontend: Open `frontend/index.html` in your browser (update API URL in `app.js`)

### Docker Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/NIKHIL-DWIVEDI/AInews.git
   cd AInews
   ```

2. **Create environment file**
   ```bash
   # Create .env.development with your API keys
   echo "NEWS_API_KEY=your_newsapi_key_here" > .env.development
   echo "GROQ_API_KEY=your_groq_api_key_here" >> .env.development
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the services**
   - API: http://localhost:8001
   - API Docs: http://localhost:8001/docs
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/admin)

5. **Stop the services**
   ```bash
   docker-compose down
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env.development` file in the project root with the following variables:

```env
# Required
NEWS_API_KEY=your_newsapi_key_here
GROQ_API_KEY=your_groq_api_key_here

# Optional (defaults provided in config.py)
# LLM_MODEL=llama-3.3-70b-versatile
# LLM_TEMPERATURE=0.7
# LLM_MAX_TOKENS=1000
```

### Application Configuration

Configuration is managed in `app/config.py`. Key settings include:

- **NewsAPI Configuration**: Base URLs for top headlines and everything endpoints
- **LLM Configuration**: Model selection, temperature, and token limits
- **Embedding Model**: Sentence transformer model for generating embeddings

## 📖 Usage

### Using the Web Interface

1. Open the frontend (`frontend/index.html`) in your browser
2. Update the API URL in `frontend/app.js` if not using default (localhost:8000)
3. Use the three main features:
   - **Fetch News**: Get latest news by category and country
   - **Search**: Perform semantic search on stored articles
   - **Ask Question**: Get AI-powered answers based on news context

### Using the API Directly

#### Fetch News
```bash
curl -X POST "http://localhost:8001/fetch-news" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence",
    "country": "us",
    "category": "technology",
    "page_size": 10,
    "page": 1
  }'
```

#### Search Articles
```bash
curl -X POST "http://localhost:8001/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning trends",
    "top_k": 5
  }'
```

#### Ask a Question
```bash
curl -X POST "http://localhost:8001/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the latest developments in AI?",
    "top_k": 5
  }'
```

#### Get Statistics
```bash
curl "http://localhost:8001/stats"
```

#### Get All Articles
```bash
curl "http://localhost:8001/articles?limit=10"
```

#### Clear All Data
```bash
curl -X DELETE "http://localhost:8001/clear"
```

## 📚 API Documentation

Once the application is running, you can access:

- **Interactive API Docs (Swagger UI)**: http://localhost:8001/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8001/redoc
- **OpenAPI Schema**: http://localhost:8001/openapi.json

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and API info |
| GET | `/stats` | Get database statistics |
| POST | `/fetch-news` | Fetch news articles from NewsAPI |
| POST | `/search` | Search articles using semantic similarity |
| POST | `/ask` | Ask a question and get AI-powered answer |
| GET | `/articles` | Get all stored articles (with pagination) |
| DELETE | `/clear` | Clear all stored data |
| GET | `/metrics` | Prometheus metrics endpoint |

## ☸️ Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured
- Docker image built and pushed (or use local registry)

### Deploy to Kubernetes

1. **Create secrets for API keys**
   ```bash
   kubectl create secret generic news-assistant-secrets \
     --from-literal=NEWS_API_KEY=your_newsapi_key \
     --from-literal=GROQ_API_KEY=your_groq_api_key
   ```

2. **Build and load Docker image** (for local clusters)
   ```bash
   docker build -t news-assistant:latest .
   
   # For minikube
   minikube image load news-assistant:latest
   
   # For kind
   kind load docker-image news-assistant:latest
   ```

3. **Deploy the application**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

4. **Check deployment status**
   ```bash
   kubectl get pods
   kubectl get services
   ```

5. **Access the application**
   ```bash
   # For NodePort service
   kubectl get service news-assistant-service
   
   # For minikube
   minikube service news-assistant-service
   ```

### Kubernetes Configuration

The Kubernetes manifests include:

- **Deployment**: 2 replicas with resource limits and health checks
- **Service**: NodePort service exposing port 8001
- **Secrets**: Secure storage of API keys
- **Resource Limits**: 
  - Requests: 256Mi memory, 250m CPU
  - Limits: 512Mi memory, 500m CPU

## 📊 Monitoring

The application includes built-in monitoring with Prometheus and Grafana.

### Metrics Collected

- **Articles Fetched**: Counter of articles fetched by source and category
- **Articles Stored**: Counter of articles successfully stored
- **RAG Queries**: Counter of RAG queries by type (search/qa)
- **RAG Query Latency**: Histogram of query processing time
- **LLM API Latency**: Histogram of LLM API call duration

### Accessing Monitoring

When running with Docker Compose:

1. **Prometheus**: http://localhost:9090
   - View metrics and create queries
   - Check targets: http://localhost:9090/targets

2. **Grafana**: http://localhost:3000
   - Default credentials: admin/admin
   - Pre-configured dashboards in `grafana/provisioning/`
   - Prometheus datasource auto-configured

### Custom Metrics

Add custom metrics in `app/metrics.py` and use them in your services:

```python
from app.metrics import my_custom_metric
my_custom_metric.labels(label_name="value").inc()
```

## 📁 Project Structure

```
AInews/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── main.py                # FastAPI application entry point
│   ├── metrics.py             # Prometheus metrics definitions
│   ├── models.py              # Data models (Article class)
│   ├── schemas.py             # Pydantic schemas for API
│   ├── services/
│   │   ├── __init__.py
│   │   ├── news_fetcher.py    # NewsAPI integration
│   │   ├── rag_service.py     # RAG and vector search
│   │   ├── llm_service.py     # LLM integration (Groq)
│   │   └── storage.py         # Local JSON storage
│   └── manual_testing/        # Manual test scripts
├── frontend/
│   ├── index.html             # Web interface
│   ├── app.js                 # Frontend JavaScript
│   └── style.css              # Styling
├── k8s/
│   ├── deployment.yaml        # Kubernetes deployment
│   └── service.yaml           # Kubernetes service
├── grafana/
│   └── provisioning/          # Grafana configuration
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image definition
├── requirements.txt           # Python dependencies
├── prometheus.yml             # Prometheus configuration
└── README.md                  # This file
```

## 🛠 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.11**: Core programming language
- **Uvicorn**: ASGI server for running FastAPI

### AI/ML
- **Groq**: LLM provider for question answering
- **LangChain**: Framework for LLM applications
- **Sentence Transformers**: Generate embeddings for semantic search
- **ChromaDB**: Vector database for storing embeddings

### Data & Storage
- **NewsAPI**: External news data source
- **JSON**: Local file storage for articles

### Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **prometheus-fastapi-instrumentator**: FastAPI metrics integration

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Kubernetes**: Container orchestration at scale

### Frontend
- **HTML5/CSS3**: Web interface structure and styling
- **Vanilla JavaScript**: Frontend interactivity

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR
- Write clear, descriptive commit messages

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists
2. Create a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Add relevant labels

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **NIKHIL-DWIVEDI** - [GitHub Profile](https://github.com/NIKHIL-DWIVEDI)

## 🙏 Acknowledgments

- [NewsAPI](https://newsapi.org/) for providing news data
- [Groq](https://groq.com/) for LLM inference
- [LangChain](https://langchain.com/) for LLM orchestration
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework

## 📞 Support

For support and questions:
- Open an issue in the GitHub repository
- Check existing documentation in `/docs`
- Review API documentation at `/docs` endpoint

---

**Made with ❤️ using AI and open source technologies**
