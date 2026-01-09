#!/usr/bin/env python3
"""
Direct test of the backend API to verify it's working
"""

import requests
import json
import time

def test_backend():
    base_url = "http://localhost:8000"
    
    print("🚀 Testing Backend API...")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Features: {data.get('features_available', [])}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Failed: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Failed: {e}")
    
    # Test 3: Analysis endpoint
    print("\n3. Testing Analysis Endpoint...")
    test_data = {
        "explanation": "A binary search tree is a data structure where each node has at most two children. The left child contains values smaller than the parent node, and the right child contains values larger than the parent node.",
        "topic": "binary search tree",
        "subject": "computer science"
    }
    
    try:
        print(f"   Sending: {test_data['topic']}")
        response = requests.post(
            f"{base_url}/api/v1/analyze", 
            json=test_data, 
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('success')}")
            print(f"   Topic: {data.get('topic')}")
            
            if data.get('success'):
                student_analysis = data.get('student_analysis', {})
                print(f"   Word count: {student_analysis.get('word_count')}")
                print(f"   Key terms: {len(student_analysis.get('key_terms', []))}")
                
                concept_analysis = data.get('concept_analysis', {})
                print(f"   Similarity: {concept_analysis.get('similarity_score', 0):.2f}")
                print(f"   Correct concepts: {len(concept_analysis.get('correct_concepts', []))}")
                
                print("   ✅ Analysis successful!")
            else:
                print(f"   ❌ Analysis failed: {data.get('error')}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   Failed: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Backend test complete!")

if __name__ == "__main__":
    test_backend()