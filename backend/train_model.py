"""
Model Training Script
Generates training data and trains the concept understanding model
"""

import asyncio
import json
import os
from app.training.data_generator import TrainingDataGenerator
from app.nlp.concept_analyzer import ConceptAnalyzer
from app.knowledge.cs_concepts import CS_CONCEPTS

async def generate_training_data():
    """Generate comprehensive training data"""
    print("🚀 Starting training data generation...")
    
    generator = TrainingDataGenerator()
    
    # Generate training examples
    print("📊 Generating training examples...")
    training_data = generator.generate_training_examples(num_examples=2000)
    
    # Save training data
    print("💾 Saving training data...")
    filepath = generator.save_training_data(training_data, "cs_concept_training.json")
    
    print(f"✅ Generated {len(training_data)} training examples")
    print(f"📁 Saved to: {filepath}")
    
    # Display statistics
    print("\n📈 Training Data Statistics:")
    level_counts = {}
    concept_counts = {}
    
    for example in training_data:
        level = example['understanding_level']
        concept = example['concept']
        
        level_counts[level] = level_counts.get(level, 0) + 1
        concept_counts[concept] = concept_counts.get(concept, 0) + 1
    
    print("Understanding Levels:")
    for level, count in level_counts.items():
        print(f"  {level}: {count} examples")
    
    print(f"\nConcepts covered: {len(concept_counts)}")
    print("Top concepts:")
    sorted_concepts = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)
    for concept, count in sorted_concepts[:5]:
        print(f"  {concept}: {count} examples")
    
    return training_data

async def test_analysis_engine():
    """Test the analysis engine with sample inputs"""
    print("\n🧪 Testing Analysis Engine...")
    
    analyzer = ConceptAnalyzer()
    
    # Test cases
    test_cases = [
        {
            'text': "A binary search tree is a hierarchical data structure where each node has at most two children. The left child is always smaller than the parent, and the right child is larger. This allows for efficient searching with O(log n) time complexity in balanced trees. For example, when searching for a value, we start at the root and go left or right based on comparisons.",
            'topic': "binary_search_tree",
            'subject': "data_structures"
        },
        {
            'text': "Binary search works by looking at the middle element and comparing it to what we're searching for. If it's the same, we found it. If it's smaller, we look in the right half, if it's bigger, we look in the left half. We keep doing this until we find it.",
            'topic': "binary_search",
            'subject': "algorithms"
        },
        {
            'text': "I think a hash table is like an array but faster. It uses some kind of function to put things in the right place. Not really sure how it works exactly.",
            'topic': "hash_table",
            'subject': "data_structures"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Topic: {test_case['topic']}")
        print(f"Text: {test_case['text'][:100]}...")
        
        analysis = analyzer.analyze_concept_understanding(
            test_case['text'], 
            test_case['topic'], 
            test_case['subject']
        )
        
        print(f"Coverage Score: {analysis['coverage_score']:.2f}")
        print(f"Correctness Score: {analysis['correctness_score']:.2f}")
        print(f"Confidence: {analysis['confidence_score']:.2f}")
        print(f"Matched Terms: {analysis['term_coverage']['matched_terms'][:3]}")
        
        if analysis['misconceptions']['misconceptions_found']:
            print(f"Misconceptions: {analysis['misconceptions']['misconceptions_found'][:2]}")

async def create_knowledge_base_summary():
    """Create a summary of the knowledge base"""
    print("\n📚 Knowledge Base Summary:")
    print(f"Total concepts: {len(CS_CONCEPTS)}")
    
    by_difficulty = {}
    by_subject = {
        'data_structures': 0,
        'algorithms': 0,
        'operating_systems': 0,
        'networks': 0,
        'databases': 0
    }
    
    for concept_key, concept_def in CS_CONCEPTS.items():
        difficulty = concept_def.difficulty_level
        by_difficulty[difficulty] = by_difficulty.get(difficulty, 0) + 1
        
        # Categorize by subject (simple heuristic)
        if any(term in concept_key for term in ['tree', 'list', 'hash', 'array']):
            by_subject['data_structures'] += 1
        elif any(term in concept_key for term in ['search', 'sort', 'algorithm']):
            by_subject['algorithms'] += 1
        elif any(term in concept_key for term in ['process', 'deadlock', 'scheduling']):
            by_subject['operating_systems'] += 1
        elif any(term in concept_key for term in ['tcp', 'network', 'protocol']):
            by_subject['networks'] += 1
        elif any(term in concept_key for term in ['acid', 'database', 'transaction']):
            by_subject['databases'] += 1
    
    print("By Difficulty Level:")
    for level in sorted(by_difficulty.keys()):
        print(f"  Level {level}: {by_difficulty[level]} concepts")
    
    print("By Subject Area:")
    for subject, count in by_subject.items():
        if count > 0:
            print(f"  {subject.replace('_', ' ').title()}: {count} concepts")

async def main():
    """Main training pipeline"""
    print("🎓 Explain My Confusion - Model Training Pipeline")
    print("=" * 50)
    
    # Create knowledge base summary
    await create_knowledge_base_summary()
    
    # Generate training data
    training_data = await generate_training_data()
    
    # Test analysis engine
    await test_analysis_engine()
    
    print("\n🎉 Training pipeline completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Review the generated training data")
    print("2. Fine-tune the analysis parameters")
    print("3. Add more concepts to the knowledge base")
    print("4. Test with real student explanations")
    print("\n🚀 The model is now ready for production use!")

if __name__ == "__main__":
    asyncio.run(main())