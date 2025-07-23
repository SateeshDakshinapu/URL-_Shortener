# 🔗 URL Shortener Service

## Overview
Build and run a simple URL shortening service — similar to Bitly or TinyURL — with endpoints for shortening, redirecting, and tracking link analytics. This project showcases a compact but fully functional backend API system.

## ✅ Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### 🚀 Setup (Takes < 5 minutes)
bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
pip install -r requirements.txt
python -m flask --app app.main run


- API: http://localhost:5000
- Run tests: pytest

## 📦 What's Included
- ✅ Flask app structure
- ✅ Health check endpoint
- ✅ Placeholder tests
- ✅ Extensible codebase

## 🧱 Core Requirements

1. *POST /api/shorten*
   - Accepts: JSON with url
   - Returns: 6-char code + short URL
   - Stores mapping

2. *GET /<short_code>*
   - Redirects to original URL
   - 404 if invalid
   - Increments click count

3. *GET /api/stats/<short_code>*
   - Returns: original URL, click count, creation time

## ⚙ Technical Specs
- Validate URLs
- 6-char alphanumeric short codes
- In-memory store
- Thread-safe
- Handle errors
- At least 5 tests

## 📡 Example Usage
bash
curl -X POST http://localhost:5000/api/shorten -H "Content-Type: application/json" -d '{"url": "https://www.example.com/long/url"}'
curl -L http://localhost:5000/abc123
curl http://localhost:5000/api/stats/abc123

