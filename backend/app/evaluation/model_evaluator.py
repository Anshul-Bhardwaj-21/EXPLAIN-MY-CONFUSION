"""
Model Evaluation System
Evaluates the performance of the concept understanding analysis
"""

import json
import statistics
from typing import Dict, List, Tuple
from app.nlp.concept_analyzer import ConceptAnalyzer
from app.training.data_generator import TrainingDataGenerator

class ModelEvaluator:
    """
    Evaluates model performance on test data
    """
    
    def __init__(self):
        self.analyzer = ConceptAnalyzer()
        self.generator = TrainingDataGenerator()
    
    def evaluate_on_test_data(self, test_data_path: str = None) -> Dict:
        """
        Evaluate model performance on test dataset
        """
        if test_data_path is None:
            # Generate test data if not provided
            print("Generating test data...")
            test_data = self.generator.generate_training_examples(num_examples=200)
        else:
            with open(test_data_path, 'r') as f:
                test_data = json.load(f)
        
        results = {
            'total_examples': len(test_data),
            'accuracy_scores': [],
            'coverage_scores': [],
            'correctness_scores': [],
            'confidence_scores': [],
            'by_understanding_level': {},
            'by_concept': {},
            'confusion_matrix': {
                'high': {'high': 0, 'medium': 0, 'low': 0, 'misconception': 0},
                'medium': {'high': 0, 'medium': 0, 'low': 0, 'misconception': 0},
                'low': {'high': 0, 'medium': 0, 'low': 0, 'misconception': 0},
                'misconception': {'high': 0, 'medium': 0, 'low': 0, 'misconception': 0}
            }
        }
        
        print(f"Evaluating on {len(test_data)} examples...")
        
        for i, example in enumerate(test_data):
            if i % 50 == 0:
                print(f"Progress: {i}/{len(test_data)}")
            
            # Run analysis
            analysis = self.analyzer.analyze_concept_understanding(
                example['text'],
                example['concept'].lower().replace(' ', '_'),
                self._get_subject_for_concept(example['concept'])
            )
            
            # Compare with ground truth
            ground_truth = example['labels']
            predicted_level = self._classify_understanding_level(analysis)
            actual_level = example['understanding_level']
            
            # Update confusion matrix
            results['confusion_matrix'][actual_level][predicted_level] += 1
            
            # Calculate accuracy metrics
            coverage_accuracy = 1 - abs(analysis['coverage_score'] - ground_truth['coverage_score'])
            correctness_accuracy = 1 - abs(analysis['correctness_score'] - ground_truth['correctness_score'])
            
            results['coverage_scores'].append(coverage_accuracy)
            results['correctness_scores'].append(correctness_accuracy)
            results['confidence_scores'].append(analysis['confidence_score'])
            
            # Track by understanding level
            if actual_level not in results['by_understanding_level']:
                results['by_understanding_level'][actual_level] = {
                    'count': 0,
                    'coverage_accuracy': [],
                    'correctness_accuracy': []
                }
            
            results['by_understanding_level'][actual_level]['count'] += 1
            results['by_understanding_level'][actual_level]['coverage_accuracy'].append(coverage_accuracy)
            results['by_understanding_level'][actual_level]['correctness_accuracy'].append(correctness_accuracy)
            
            # Track by concept
            concept = example['concept']
            if concept not in results['by_concept']:
                results['by_concept'][concept] = {
                    'count': 0,
                    'coverage_accuracy': [],
                    'correctness_accuracy': []
                }
            
            results['by_concept'][concept]['count'] += 1
            results['by_concept'][concept]['coverage_accuracy'].append(coverage_accuracy)
            results['by_concept'][concept]['correctness_accuracy'].append(correctness_accuracy)
        
        # Calculate summary statistics
        results['summary'] = {
            'mean_coverage_accuracy': statistics.mean(results['coverage_scores']),
            'mean_correctness_accuracy': statistics.mean(results['correctness_scores']),
            'mean_confidence': statistics.mean(results['confidence_scores']),
            'classification_accuracy': self._calculate_classification_accuracy(results['confusion_matrix'])
        }
        
        return results
    
    def _classify_understanding_level(self, analysis: Dict) -> str:
        """
        Classify understanding level based on analysis scores
        """
        coverage = analysis['coverage_score']
        correctness = analysis['correctness_score']
        misconceptions = analysis['misconceptions']['severity']
        
        if misconceptions > 0.3:
            return 'misconception'
        elif coverage >= 0.7 and correctness >= 0.8:
            return 'high'
        elif coverage >= 0.4 and correctness >= 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _get_subject_for_concept(self, concept_name: str) -> str:
        """
        Map concept to subject area
        """
        concept_lower = concept_name.lower()
        
        if any(term in concept_lower for term in ['tree', 'list', 'hash', 'array']):
            return 'data_structures'
        elif any(term in concept_lower for term in ['search', 'sort', 'algorithm']):
            return 'algorithms'
        elif any(term in concept_lower for term in ['process', 'deadlock', 'scheduling']):
            return 'operating_systems'
        elif any(term in concept_lower for term in ['tcp', 'network', 'protocol']):
            return 'computer_networks'
        elif any(term in concept_lower for term in ['acid', 'database', 'transaction']):
            return 'databases'
        else:
            return 'data_structures'  # default
    
    def _calculate_classification_accuracy(self, confusion_matrix: Dict) -> float:
        """
        Calculate overall classification accuracy
        """
        total_correct = 0
        total_examples = 0
        
        for actual_level in confusion_matrix:
            for predicted_level in confusion_matrix[actual_level]:
                count = confusion_matrix[actual_level][predicted_level]
                total_examples += count
                if actual_level == predicted_level:
                    total_correct += count
        
        return total_correct / total_examples if total_examples > 0 else 0
    
    def print_evaluation_report(self, results: Dict):
        """
        Print a comprehensive evaluation report
        """
        print("\n" + "="*60)
        print("📊 MODEL EVALUATION REPORT")
        print("="*60)
        
        summary = results['summary']
        print(f"\n🎯 OVERALL PERFORMANCE:")
        print(f"  Classification Accuracy: {summary['classification_accuracy']:.3f}")
        print(f"  Coverage Accuracy: {summary['mean_coverage_accuracy']:.3f}")
        print(f"  Correctness Accuracy: {summary['mean_correctness_accuracy']:.3f}")
        print(f"  Mean Confidence: {summary['mean_confidence']:.3f}")
        
        print(f"\n📈 CONFUSION MATRIX:")
        print("Actual \\ Predicted | High   | Medium | Low    | Misconc")
        print("-" * 55)
        
        for actual in ['high', 'medium', 'low', 'misconception']:
            row = f"{actual:15} |"
            for predicted in ['high', 'medium', 'low', 'misconception']:
                count = results['confusion_matrix'][actual][predicted]
                row += f" {count:6} |"
            print(row)
        
        print(f"\n📚 PERFORMANCE BY UNDERSTANDING LEVEL:")
        for level, stats in results['by_understanding_level'].items():
            coverage_acc = statistics.mean(stats['coverage_accuracy'])
            correctness_acc = statistics.mean(stats['correctness_accuracy'])
            print(f"  {level.capitalize():12}: Coverage={coverage_acc:.3f}, Correctness={correctness_acc:.3f} ({stats['count']} examples)")
        
        print(f"\n🧠 PERFORMANCE BY CONCEPT:")
        for concept, stats in results['by_concept'].items():
            if stats['count'] > 0:
                coverage_acc = statistics.mean(stats['coverage_accuracy'])
                correctness_acc = statistics.mean(stats['correctness_accuracy'])
                print(f"  {concept:20}: Coverage={coverage_acc:.3f}, Correctness={correctness_acc:.3f} ({stats['count']} examples)")
        
        print("\n" + "="*60)
    
    def run_comprehensive_evaluation(self):
        """
        Run a comprehensive evaluation of the model
        """
        print("🔬 Starting Comprehensive Model Evaluation...")
        
        # Evaluate on test data
        results = self.evaluate_on_test_data()
        
        # Print detailed report
        self.print_evaluation_report(results)
        
        # Save results
        with open('app/training/data/evaluation_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Evaluation results saved to: app/training/data/evaluation_results.json")
        
        return results

if __name__ == "__main__":
    evaluator = ModelEvaluator()
    evaluator.run_comprehensive_evaluation()