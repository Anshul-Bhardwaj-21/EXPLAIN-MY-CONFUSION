/**
 * API service for real backend communication
 * Handles HTTP requests to the real NLP analysis backend
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function makeRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        response.status
      );
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    
    // Network or other errors
    throw new ApiError('Network error or server unavailable', 0);
  }
}

export async function analyzeExplanation(explanation, topic, subject = null) {
  const payload = {
    explanation,
    topic,
  };
  
  if (subject) {
    payload.subject = subject;
  }
  
  return makeRequest('/analyze', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function getTopicOverview(topic) {
  return makeRequest(`/topic-overview/${encodeURIComponent(topic)}`);
}

export async function checkHealth() {
  const response = await fetch('http://localhost:8000/health');
  return response.json();
}