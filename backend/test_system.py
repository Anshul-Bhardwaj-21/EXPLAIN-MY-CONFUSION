#!/usr/bin/env python3
"""
Comprehensive System Test Script
Tests all components of the Explain My Confusion system
"""

import sys
import os
import json
import asyncio
from typing import Dict, Any

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_knowledge_base():
    """Test the knowledge base components"""
    print("🧠 Testing Knowledge Base Components...")
    
    try:
        from app.knowledge.cs_concepts import CS_CONCEPTS, get_concept_by_name
        from app.knowledge.wikipedia_kb import WikipediaKnowledgeBase
        
        # Test CS concepts
        print(f"  ✅ CS Concepts loaded: {len(CS_CONCEPTS)} concepts")
        
        # Test specific concept retrieval
        bst_concept = get_concept_by_name("binary_search_tree")
        if bst_concept:
            print(f"  ✅ Binary Search Tree concept: {len(bst_concept.key_terms)} key terms")
        else:
            print("  ❌ Failed to retrieve Binary Search Tree concept")
        
        # Test Wikipedia knowledge base
        kb = WikipediaKnowledgeBase()
        print("  ✅ Wikipedia Knowledge Base initialized")
        
        # Test Wikipedia search
        search_results = kb.search_topics("binary search tree", max_results=3)
        print(f"  ✅ Wikipedia search returned {len(search_results)} results")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Knowledge Base test failed: {e}")
        return False

def test_nlp_pipeline():
    """Test the NLP processing pipeline"""
    print("🔤 Testing NLP Pipeline...")
    
    try:
        from app.nlp.preprocess import RealNLPProcessor
        from app.nlp.embeddings import EmbeddingService
        from app.nlp.dependency import DependencyParser
        
        # Test preprocessor
        processor = RealNLPProcessor()
        test_text = "A binary search tree is a hierarchical data structure where each node has at most two children."
        
        # Test tokenization
        tokens = processor.tokenize(test_text)
        print(f"  ✅ Tokenization: {len(tokens)} tokens")
        
        # Test key term extraction
        key_terms = processor.extract_key_terms(test_text)
        print(f"  ✅ Key term extraction: {len(key_terms)} terms")
        
        # Test structure analysis
        structure = processor.analyze_text_structure(test_text)
        print(f"  ✅ Structure analysis: {structure['word_count']} words, {structure['sentence_count']} sentences")
        
        # Test embeddings service
        embedding_service = EmbeddingService()
        similarity = embedding_service.compute_similarity(test_text, "Binary trees organize data hierarchically")
        print(f"  ✅ Semantic similarity: {similarity:.3f}")
        
        # Test dependency parser
        parser = DependencyParser()
        relationships = parser.find_concept_relationships(test_text)
        print(f"  ✅ Concept relationships: {len(relationships)} found")
        
        return True
        
    except Exception as e:
        print(f"  ❌ NLP Pipeline test failed: {e}")
        return False

def test_analysis_engine():
    """Test the concept analysis engine"""
    print("⚙️ Testing Analysis Engine...")
    
    try:
        from app.analysis.concept_engine import ConceptComparisonEngine
        
        engine = ConceptComparisonEngine()
        
        # Test analysis with sample input
        test_explanation = """
        A binary search tree is a tree data structure where each node has at most two children.
        The left child contains values smaller than the parent, and the right child contains
        values larger than the parent. This ordering property makes searching efficient.
        """
        
        result = engine.analyze_explanation(
            student_text=test_explanation,
            topic="binary search tree",
            subject="data_structures"
        )
        
        if result.get('success'):
            print(f"  ✅ Analysis successful")
            print(f"  ✅ Coverage score: {result['student_analysis']['key_terms'][:3]}...")
            print(f"  ✅ Reference found: {result['reference_info']['title']}")
            print(f"  ✅ Similarity: {result['concept_analysis']['similarity_score']:.3f}")
        else:
            print(f"  ❌ Analysis failed: {result.get('error', 'Unknown error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Analysis Engine test failed: {e}")
        return False

def test_training_system():
    """Test the training data generation and evaluation"""
    print("📊 Testing Training System...")
    
    try:
        from app.training.data_generator import TrainingDataGenerator
        from app.evaluation.model_evaluator import ModelEvaluator
        
        # Test data generation
        generator = TrainingDataGenerator()
        sample_data = generator.generate_training_examples(num_examples=20)
        print(f"  ✅ Generated {len(sample_data)} training examples")
        
        # Verify data structure
        if sample_data:
            example = sample_data[0]
            required_keys = ['text', 'concept', 'understanding_level', 'labels']
            if all(key in example for key in required_keys):
                print("  ✅ Training data structure is valid")
            else:
                print("  ❌ Training data structure is invalid")
                return False
        
        # Test evaluation system
        evaluator = ModelEvaluator()
        print("  ✅ Model evaluator initialized")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Training System test failed: {e}")
        return False

async def test_api_endpoints():
    """Test the FastAPI endpoints"""
    print("🌐 Testing API Endpoints...")
    
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        if response.status_code == 200:
            print("  ✅ Health endpoint working")
        else:
            print(f"  ❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test root endpoint
        response = client.get("/")
        if response.status_code == 200:
            print("  ✅ Root endpoint working")
        else:
            print(f"  ❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test analysis endpoint
        test_payload = {
            "explanation": "A binary search tree is a tree where left nodes are smaller and right nodes are bigger.",
            "topic": "binary search tree",
            "subject": "data_structures"
        }
        
        response = client.post("/api/v1/analyze", json=test_payload)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("  ✅ Analysis endpoint working")
                print(f"  ✅ Analysis returned: {result['topic']}")
            else:
                print(f"  ❌ Analysis endpoint returned error: {result.get('error')}")
                return False
        else:
            print(f"  ❌ Analysis endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ API Endpoints test failed: {e}")
        return False

def test_data_integrity():
    """Test data integrity and consistency"""
    print("🔍 Testing Data Integrity...")
    
    try:
        # Check if training data exists and is valid
        training_data_path = "app/training/data/cs_concept_training.json"
        if os.path.exists(training_data_path):
            with open(training_data_path, 'r') as f:
                training_data = json.load(f)
            print(f"  ✅ Training data found: {len(training_data)} examples")
            
            # Validate data structure
            if training_data:
                example = training_data[0]
                if 'labels' in example and 'understanding_score' in example['labels']:
                    print("  ✅ Training data structure is valid")
                else:
                    print("  ❌ Training data structure is invalid")
                    return False
        else:
            print("  ⚠️ Training data file not found (will be generated on first run)")
        
        # Check evaluation results
        eval_results_path = "app/training/data/evaluation_results.json"
        if os.path.exists(eval_results_path):
            with open(eval_results_path, 'r') as f:
                eval_results = json.load(f)
            print(f"  ✅ Evaluation results found: {eval_results['total_examples']} examples")
            
            # Check performance metrics
            summary = eval_results.get('summary', {})
            if 'mean_coverage_accuracy' in summary:
                coverage_acc = summary['mean_coverage_accuracy']
                correctness_acc = summary['mean_correctness_accuracy']
                print(f"  ✅ Performance metrics: Coverage={coverage_acc:.3f}, Correctness={correctness_acc:.3f}")
            else:
                print("  ❌ Performance metrics not found")
                return False
        else:
            print("  ⚠️ Evaluation results not found (will be generated on first evaluation)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Data Integrity test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all system tests"""
    print("🚀 Starting Comprehensive System Test")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("Knowledge Base", test_knowledge_base),
        ("NLP Pipeline", test_nlp_pipeline),
        ("Analysis Engine", test_analysis_engine),
        ("Training System", test_training_system),
        ("Data Integrity", test_data_integrity),
    ]
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test crashed: {e}")
            test_results.append((test_name, False))
    
    # Test API endpoints (async)
    print(f"\nAPI Endpoints:")
    try:
        result = asyncio.run(test_api_endpoints())
        test_results.append(("API Endpoints", result))
    except Exception as e:
        print(f"  ❌ API Endpoints test crashed: {e}")
        test_results.append(("API Endpoints", False))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)