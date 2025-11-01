// app.js

// Configuration - Change this to your API URL
const API_BASE_URL = 'http://localhost:8000';
// If using Kubernetes: const API_BASE_URL = 'http://news-assistant.local';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    setupEventListeners();
    
    // Refresh stats every 30 seconds
    setInterval(loadStats, 30000);
});

// Tab Switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}Tab`).classList.add('active');
    
    // Mark button as active
    event.target.classList.add('active');
}

// Load Stats
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();
        
        document.getElementById('storageCount').textContent = data.total_articles_stored || 0;
        document.getElementById('vectorCount').textContent = data.total_articles_in_vectordb || 0;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Setup Event Listeners
function setupEventListeners() {
    document.getElementById('fetchForm').addEventListener('submit', handleFetchNews);
    document.getElementById('searchForm').addEventListener('submit', handleSearch);
    document.getElementById('askForm').addEventListener('submit', handleAsk);
}

// Show/Hide Loading Spinner
function showLoading() {
    document.getElementById('loadingSpinner').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingSpinner').classList.remove('active');
}

// Handle Fetch News
async function handleFetchNews(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        category: formData.get('category') || null,
        country: formData.get('country'),
        page_size: parseInt(formData.get('pageSize'))
    };
    
    showLoading();
    const resultsDiv = document.getElementById('fetchResults');
    resultsDiv.innerHTML = '';
    
    try {
        const response = await fetch(`${API_BASE_URL}/fetch-news`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const articles = await response.json();
        
        resultsDiv.innerHTML = `
            <div class="success">
                ✅ Successfully fetched ${articles.length} articles!
            </div>
        `;
        
        articles.forEach(article => {
            const articleEl = createArticleElement(article);
            resultsDiv.appendChild(articleEl);
        });
        
        // Refresh stats
        loadStats();
        
    } catch (error) {
        resultsDiv.innerHTML = `
            <div class="error">
                ❌ Error: ${error.message}
            </div>
        `;
    } finally {
        hideLoading();
    }
}

// Handle Search
async function handleSearch(e) {
    e.preventDefault();
    
    const query = document.getElementById('searchQuery').value;
    const topK = parseInt(document.getElementById('topK').value);
    
    showLoading();
    const resultsDiv = document.getElementById('searchResults');
    resultsDiv.innerHTML = '';
    
    try {
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query, top_k: topK })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        resultsDiv.innerHTML = `
            <div class="success">
                🔍 Found ${data.total_results} relevant articles
            </div>
        `;
        
        data.results.forEach(result => {
            const resultEl = createSearchResultElement(result);
            resultsDiv.appendChild(resultEl);
        });
        
    } catch (error) {
        resultsDiv.innerHTML = `
            <div class="error">
                ❌ Error: ${error.message}
            </div>
        `;
    } finally {
        hideLoading();
    }
}

// Handle Ask Question
async function handleAsk(e) {
    e.preventDefault();
    
    const question = document.getElementById('question').value;
    const topK = parseInt(document.getElementById('sourcesCount').value);
    
    showLoading();
    const resultsDiv = document.getElementById('askResults');
    resultsDiv.innerHTML = '';
    
    try {
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question, top_k: topK })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const answerEl = createAnswerElement(data);
        resultsDiv.appendChild(answerEl);
        
    } catch (error) {
        resultsDiv.innerHTML = `
            <div class="error">
                ❌ Error: ${error.message}
            </div>
        `;
    } finally {
        hideLoading();
    }
}

// Create Article Element
function createArticleElement(article) {
    const div = document.createElement('div');
    div.className = 'result-item';
    
    div.innerHTML = `
        <div class="result-title">${article.title}</div>
        <div class="result-meta">
            <span class="result-source">📰 ${article.source_name}</span>
            <span>${article.published_at}</span>
            ${article.author ? `<span>✍️ ${article.author}</span>` : ''}
        </div>
        <div class="result-content">${article.description || 'No description available'}</div>
        <a href="${article.url}" target="_blank" class="result-url">Read full article →</a>
    `;
    
    return div;
}

// Create Search Result Element
function createSearchResultElement(result) {
    const div = document.createElement('div');
    div.className = 'result-item';
    
    div.innerHTML = `
        <div class="result-title">${result.title}</div>
        <div class="result-meta">
            <span class="result-source">📰 ${result.source_name}</span>
            <span class="result-score">Relevance: ${(result.similarity_score * 100).toFixed(1)}%</span>
        </div>
        <div class="result-content">${result.content_preview}</div>
        <a href="${result.url}" target="_blank" class="result-url">Read full article →</a>
    `;
    
    return div;
}

// Create Answer Element
function createAnswerElement(data) {
    const div = document.createElement('div');
    div.className = 'answer-box';
    
    let sourcesHTML = '';
    if (data.sources && data.sources.length > 0) {
        sourcesHTML = `
            <div class="sources-title">📚 Sources:</div>
            ${data.sources.map((source, idx) => `
                <div class="source-item">
                    <strong>${idx + 1}. ${source.title}</strong><br>
                    <small>📰 ${source.source} | Relevance: ${(source.relevance * 100).toFixed(1)}%</small><br>
                    <a href="${source.url}" target="_blank" class="result-url">Read article →</a>
                </div>
            `).join('')}
        `;
    }
    
    div.innerHTML = `
        <div class="answer-text">${data.answer}</div>
        ${sourcesHTML}
    `;
    
    return div;
}