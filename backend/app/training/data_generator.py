"""
Training Data Generator
Generates synthetic training data for concept understanding analysis
"""

import random
from typing import List, Dict, Tuple
from app.knowledge.cs_concepts import CS_CONCEPTS

class TrainingDataGenerator:
    """
    Generates training examples for different levels of concept understanding
    """
    
    def __init__(self):
        self.understanding_templates = {
            'high': [
                "{concept} is {definition}. It works by {process}. For example, {example}. This is useful because {benefit}.",
                "{concept} {definition}. The key advantage is {benefit}. It operates through {process}, as seen in {example}.",
                "Understanding {concept}: {definition}. The process involves {process}. A practical example is {example}."
            ],
            'medium': [
                "{concept} is {definition}. It {process}. An example would be {example}.",
                "{concept} {definition}. This works by {process}. You can see this in {example}.",
                "A {concept} is {definition}. It {process}."
            ],
            'low': [
                "{concept} is {definition}.",
                "I think {concept} {definition}.",
                "{concept} is something that {process}.",
                "Maybe {concept} {definition}. Not sure though."
            ],
            'misconception': [
                "{concept} always {wrong_statement}. It never {correct_behavior}.",
                "{concept} is the same as {wrong_comparison}. It must {wrong_requirement}.",
                "The only way to use {concept} is {wrong_method}. It cannot {correct_capability}."
            ]
        }
        
        self.uncertainty_phrases = [
            "I think", "Maybe", "Probably", "I'm not sure", "I believe", "It seems like",
            "I guess", "Perhaps", "Might be", "Could be"
        ]
        
        self.confidence_phrases = [
            "Definitely", "Clearly", "Obviously", "Certainly", "Without doubt", "Precisely"
        ]
    
    def generate_training_examples(self, num_examples: int = 1000) -> List[Dict]:
        """
        Generate training examples for all concepts
        """
        training_data = []
        
        for concept_key, concept_def in CS_CONCEPTS.items():
            # Generate examples for each understanding level
            for level in ['high', 'medium', 'low', 'misconception']:
                examples_per_level = num_examples // (len(CS_CONCEPTS) * 4)
                
                for _ in range(examples_per_level):
                    example = self._generate_single_example(concept_def, level)
                    training_data.append(example)
        
        return training_data
    
    def _generate_single_example(self, concept_def, understanding_level: str) -> Dict:
        """
        Generate a single training example
        """
        template = random.choice(self.understanding_templates[understanding_level])
        
        # Fill in template variables
        filled_text = self._fill_template(template, concept_def, understanding_level)
        
        # Add uncertainty or confidence markers
        if understanding_level == 'low' or understanding_level == 'misconception':
            if random.random() < 0.3:
                uncertainty = random.choice(self.uncertainty_phrases)
                filled_text = f"{uncertainty}, {filled_text.lower()}"
        elif understanding_level == 'high':
            if random.random() < 0.2:
                confidence = random.choice(self.confidence_phrases)
                filled_text = f"{confidence}, {filled_text.lower()}"
        
        # Determine labels
        labels = self._generate_labels(understanding_level, concept_def)
        
        return {
            'text': filled_text,
            'concept': concept_def.name,
            'understanding_level': understanding_level,
            'labels': labels,
            'metadata': {
                'difficulty': concept_def.difficulty_level,
                'key_terms_present': self._count_key_terms(filled_text, concept_def.key_terms),
                'word_count': len(filled_text.split())
            }
        }
    
    def _fill_template(self, template: str, concept_def, understanding_level: str) -> str:
        """
        Fill template with concept-specific information
        """
        # Basic replacements
        replacements = {
            'concept': concept_def.name,
            'definition': concept_def.description,
            'process': self._get_process_description(concept_def),
            'example': random.choice(concept_def.applications) if concept_def.applications else "various applications",
            'benefit': self._get_benefit_description(concept_def)
        }
        
        # Add misconception-specific replacements
        if understanding_level == 'misconception':
            replacements.update({
                'wrong_statement': self._generate_wrong_statement(concept_def),
                'correct_behavior': self._generate_correct_behavior(concept_def),
                'wrong_comparison': self._generate_wrong_comparison(concept_def),
                'wrong_requirement': self._generate_wrong_requirement(concept_def),
                'wrong_method': self._generate_wrong_method(concept_def),
                'correct_capability': self._generate_correct_capability(concept_def)
            })
        
        # Fill template
        filled_text = template
        for key, value in replacements.items():
            if f'{{{key}}}' in filled_text:
                filled_text = filled_text.replace(f'{{{key}}}', str(value))
        
        return filled_text
    
    def _get_process_description(self, concept_def) -> str:
        """Generate process description based on concept"""
        if 'tree' in concept_def.name.lower():
            return "organizing data in a hierarchical structure with parent-child relationships"
        elif 'search' in concept_def.name.lower():
            return "systematically examining elements to find a target value"
        elif 'sort' in concept_def.name.lower():
            return "arranging elements in a specific order"
        elif 'hash' in concept_def.name.lower():
            return "using a hash function to map keys to array indices"
        else:
            return "following a systematic approach to solve the problem"
    
    def _get_benefit_description(self, concept_def) -> str:
        """Generate benefit description"""
        benefits = [
            "it provides efficient performance",
            "it solves the problem effectively",
            "it offers good time complexity",
            "it handles the requirements well"
        ]
        return random.choice(benefits)
    
    def _generate_wrong_statement(self, concept_def) -> str:
        """Generate wrong statements for misconceptions"""
        wrong_statements = [
            "has O(1) time complexity",
            "works with unsorted data",
            "never fails",
            "is the fastest approach",
            "requires no memory"
        ]
        return random.choice(wrong_statements)
    
    def _generate_correct_behavior(self, concept_def) -> str:
        """Generate correct behaviors that misconceptions deny"""
        behaviors = [
            "handle edge cases",
            "work with different data types",
            "be optimized further",
            "have trade-offs"
        ]
        return random.choice(behaviors)
    
    def _generate_wrong_comparison(self, concept_def) -> str:
        """Generate wrong comparisons"""
        comparisons = ["array", "list", "stack", "queue", "tree", "graph"]
        return random.choice([c for c in comparisons if c not in concept_def.name.lower()])
    
    def _generate_wrong_requirement(self, concept_def) -> str:
        """Generate wrong requirements"""
        requirements = [
            "always be balanced",
            "only work with integers",
            "require sorted input",
            "use recursive implementation"
        ]
        return random.choice(requirements)
    
    def _generate_wrong_method(self, concept_def) -> str:
        """Generate wrong methods"""
        methods = [
            "iterate through all elements",
            "use brute force approach",
            "check every possibility",
            "start from the beginning"
        ]
        return random.choice(methods)
    
    def _generate_correct_capability(self, concept_def) -> str:
        """Generate correct capabilities"""
        capabilities = [
            "be implemented iteratively",
            "handle dynamic data",
            "work with different data types",
            "be optimized for specific cases"
        ]
        return random.choice(capabilities)
    
    def _generate_labels(self, understanding_level: str, concept_def) -> Dict:
        """Generate training labels"""
        if understanding_level == 'high':
            return {
                'understanding_score': random.uniform(0.8, 1.0),
                'correctness_score': random.uniform(0.85, 1.0),
                'coverage_score': random.uniform(0.7, 1.0),
                'has_misconceptions': False,
                'confidence_level': 'high'
            }
        elif understanding_level == 'medium':
            return {
                'understanding_score': random.uniform(0.5, 0.8),
                'correctness_score': random.uniform(0.6, 0.85),
                'coverage_score': random.uniform(0.4, 0.7),
                'has_misconceptions': False,
                'confidence_level': 'medium'
            }
        elif understanding_level == 'low':
            return {
                'understanding_score': random.uniform(0.2, 0.5),
                'correctness_score': random.uniform(0.3, 0.6),
                'coverage_score': random.uniform(0.1, 0.4),
                'has_misconceptions': False,
                'confidence_level': 'low'
            }
        else:  # misconception
            return {
                'understanding_score': random.uniform(0.1, 0.4),
                'correctness_score': random.uniform(0.0, 0.3),
                'coverage_score': random.uniform(0.2, 0.5),
                'has_misconceptions': True,
                'confidence_level': 'low'
            }
    
    def _count_key_terms(self, text: str, key_terms: List[str]) -> int:
        """Count how many key terms are present in the text"""
        text_lower = text.lower()
        return sum(1 for term in key_terms if term.lower() in text_lower)
    
    def save_training_data(self, training_data: List[Dict], filename: str = "training_data.json"):
        """Save training data to file"""
        import json
        import os
        
        # Create training directory if it doesn't exist
        os.makedirs("app/training/data", exist_ok=True)
        
        filepath = f"app/training/data/{filename}"
        with open(filepath, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        print(f"Saved {len(training_data)} training examples to {filepath}")
        return filepath