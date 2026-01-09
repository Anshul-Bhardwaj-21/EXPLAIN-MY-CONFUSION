# 🚀 Deployment Guide - Explain My Confusion

Complete step-by-step guide to deploy and run the NLP Educational Diagnostic System.

## 📋 Prerequisites

### System Requirements
- **Python 3.14+** (tested on Python 3.14)
- **Node.js 16+** with npm
- **Windows 10/11** (tested environment)
- **Internet connection** (for Wikipedia API and model downloads)
- **4GB+ RAM** (for sentence transformers)
- **2GB+ disk space** (for models and dependencies)

### Required Tools
- Git (for cloning repository)
- Command Prompt or PowerShell
- Text editor (VS Code recommended)

## 🔧 Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note:** This will install:
- FastAPI, uvicorn (web framework)
- NLTK, sentence-transformers (NLP processing)
- Wikipedia, requests (knowledge retrieval)
- scikit-learn, numpy (machine learning)
- All other required dependencies

### Step 3: Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

### Step 4: Test Backend System
```bash
python test_system.py
```

**Expected Output:**
```
🚀 Starting Comprehensive System Test
==================================================
Knowledge Base      : ✅ PASS
NLP Pipeline        : ✅ PASS
Analysis Engine     : ✅ PASS
Training System     : ✅ PASS
Data Integrity      : ✅ PASS
API Endpoints       : ✅ PASS

Overall Result: 6/6 tests passed
🎉 ALL TESTS PASSED! System is ready for use.
```

### Step 5: Start Backend Server
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend:**
- Open browser: `http://localhost:8000`
- Should see: `{"message": "Explain My Confusion - Real NLP Analysis API", "version": "2.0.0"}`
- API docs: `http://localhost:8000/docs`

## 🎨 Frontend Setup

### Step 1: Open New Terminal/Command Prompt
Keep backend running, open new terminal window.

### Step 2: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 3: Install Node.js Dependencies
```bash
npm install
```

**Expected packages:**
- React 18+ (UI framework)
- React scripts (development tools)
- Web Vitals (performance monitoring)

### Step 4: Start Frontend Development Server
```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view explain-my-confusion in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

**Verify Frontend:**
- Browser should automatically open `http://localhost:3000`
- Should see the "Explain My Confusion" welcome page
- UI should be responsive and interactive

## 🧪 System Verification

### Test Complete System
1. **Open frontend:** `http://localhost:3000`
2. **Enter test data:**
   - Topic: "Binary Search Tree"
   - Subject: "Data Structures" (optional)
   - Explanation: "A binary search tree is a tree where left nodes are smaller and right nodes are bigger. This makes searching faster."
3. **Click "Analyze My Explanation"**
4. **Expected result:** Detailed analysis with scores and feedback

### Sample Test Cases

#### Test Case 1: Good Understanding
```
Topic: Hash Table
Explanation: A hash table uses a hash function to map keys to array indices. It provides O(1) average time complexity for insertion, deletion, and lookup operations. Collisions can occur when different keys hash to the same index, which can be resolved using chaining or open addressing.
```

#### Test Case 2: Basic Understanding
```
Topic: Quicksort
Explanation: Quicksort is a sorting algorithm that picks a pivot element and arranges other elements around it. It's faster than bubble sort.
```

#### Test Case 3: Misconception
```
Topic: Binary Search
Explanation: Binary search works on any array and always finds elements in O(1) time. It's the fastest search algorithm.
```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Backend Issues

**Issue: "No module named 'wikipedia'"**
```bash
# Solution: Install missing packages
pip install wikipedia nltk sentence-transformers scikit-learn
```

**Issue: "Resource punkt_tab not found"**
```bash
# Solution: Download NLTK data
python -c "import nltk; nltk.download('punkt_tab')"
```

**Issue: "Port 8000 already in use"**
```bash
# Solution: Use different port
python -m uvicorn app.main:app --reload --port 8001
# Update frontend API URL in src/services/api.js
```

**Issue: "sentence-transformers model download fails"**
```bash
# Solution: Manual download or use offline mode
# The system will fallback to TF-IDF similarity
```

#### Frontend Issues

**Issue: "npm install fails"**
```bash
# Solution: Clear cache and retry
npm cache clean --force
npm install
```

**Issue: "Cannot connect to backend"**
```bash
# Solution: Check backend is running on port 8000
# Verify API_BASE_URL in src/services/api.js
```

**Issue: "CORS errors"**
```bash
# Solution: Backend CORS is configured for localhost:3000
# If using different port, update backend/app/main.py
```

### Performance Issues

**Slow Analysis (>10 seconds):**
- First run downloads sentence transformer model (~90MB)
- Subsequent runs should be 2-3 seconds
- Check internet connection for Wikipedia API

**High Memory Usage:**
- Sentence transformers require ~1GB RAM
- System will fallback to TF-IDF if models fail to load

## 📊 System Status Check

### Health Check Endpoints
- **Backend Health:** `GET http://localhost:8000/health`
- **Backend Root:** `GET http://localhost:8000/`
- **API Documentation:** `http://localhost:8000/docs`

### Expected Response
```json
{
  "status": "healthy",
  "timestamp": "2026-01-06T...",
  "features_available": [
    "Wikipedia Knowledge Base",
    "NLP Processing", 
    "Wikipedia API",
    "Sentence Embeddings"
  ]
}
```

## 🔒 Security Considerations

### Development Environment
- Backend runs on all interfaces (0.0.0.0) for development
- CORS enabled for localhost:3000
- No authentication required

### Production Deployment
- Change host to 127.0.0.1 for production
- Implement proper CORS policies
- Add rate limiting and authentication
- Use HTTPS with proper certificates
- Monitor API usage and costs

## 📈 Performance Optimization

### Backend Optimization
- **Caching:** Wikipedia content is cached locally
- **Model Loading:** Sentence transformers loaded once at startup
- **Async Processing:** FastAPI handles concurrent requests
- **Error Handling:** Graceful fallbacks for failed components

### Frontend Optimization
- **Code Splitting:** React components loaded on demand
- **Lazy Loading:** Heavy components loaded when needed
- **Caching:** API responses cached in browser
- **Responsive Design:** Optimized for all screen sizes

## 🚀 Production Deployment

### Docker Deployment (Optional)
```dockerfile
# Backend Dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
# Backend .env
WIKIPEDIA_CACHE_DIR=./cache
NLTK_DATA_PATH=./nltk_data
MODEL_CACHE_DIR=./models
LOG_LEVEL=INFO

# Frontend .env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VERSION=2.0.0
```

## 📞 Support and Maintenance

### Log Files
- **Backend Logs:** Console output with INFO/ERROR levels
- **Frontend Logs:** Browser console for debugging
- **System Logs:** `logs/project_audit_log.txt`

### Monitoring
- **Health Checks:** Automated endpoint monitoring
- **Performance:** Response time tracking
- **Errors:** Exception logging and alerting
- **Usage:** API call statistics

### Updates
- **Dependencies:** Regular security updates
- **Models:** Periodic model improvements
- **Knowledge Base:** Wikipedia content auto-updates
- **Features:** Incremental feature additions

---

## ✅ Deployment Checklist

- [ ] Python 3.14+ installed
- [ ] Node.js 16+ installed
- [ ] Backend dependencies installed
- [ ] NLTK data downloaded
- [ ] Backend tests passing
- [ ] Backend server running on port 8000
- [ ] Frontend dependencies installed
- [ ] Frontend server running on port 3000
- [ ] System integration test completed
- [ ] Sample analysis working correctly

**🎉 Congratulations! Your NLP Educational Diagnostic System is now fully deployed and ready for use!**