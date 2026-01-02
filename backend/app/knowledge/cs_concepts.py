"""
Computer Science Concepts Knowledge Base
Contains structured knowledge about CS concepts, their relationships, and key indicators
"""

from typing import Dict, List, Set
from dataclasses import dataclass

@dataclass
class ConceptDefinition:
    name: str
    description: str
    key_terms: List[str]
    prerequisites: List[str]
    applications: List[str]
    common_misconceptions: List[str]
    difficulty_level: int  # 1-5 scale

# Comprehensive CS Concepts Knowledge Base
CS_CONCEPTS = {
    # Data Structures
    "binary_search_tree": ConceptDefinition(
        name="Binary Search Tree",
        description="A hierarchical data structure where each node has at most two children, with left child smaller and right child larger than parent",
        key_terms=["tree", "node", "left child", "right child", "root", "leaf", "binary", "search", "hierarchy", "parent", "traversal", "inorder", "preorder", "postorder"],
        prerequisites=["binary_tree", "recursion", "tree_traversal"],
        applications=["searching", "sorting", "database indexing", "expression parsing"],
        common_misconceptions=[
            "thinking BST is always balanced",
            "confusing with binary heap",
            "not understanding worst-case O(n) complexity"
        ],
        difficulty_level=3
    ),
    
    "linked_list": ConceptDefinition(
        name="Linked List",
        description="A linear data structure where elements are stored in nodes, each containing data and a reference to the next node",
        key_terms=["node", "pointer", "reference", "head", "tail", "next", "linear", "dynamic", "memory", "allocation"],
        prerequisites=["pointers", "memory_management"],
        applications=["dynamic arrays", "undo functionality", "music playlists", "browser history"],
        common_misconceptions=[
            "thinking it's faster than arrays for all operations",
            "not understanding memory overhead",
            "confusing with arrays"
        ],
        difficulty_level=2
    ),
    
    "hash_table": ConceptDefinition(
        name="Hash Table",
        description="A data structure that maps keys to values using a hash function for fast lookup, insertion, and deletion",
        key_terms=["hash function", "collision", "bucket", "key", "value", "chaining", "open addressing", "load factor"],
        prerequisites=["arrays", "functions"],
        applications=["dictionaries", "caching", "database indexing", "symbol tables"],
        common_misconceptions=[
            "thinking hash tables are always O(1)",
            "not understanding collision handling",
            "ignoring load factor importance"
        ],
        difficulty_level=3
    ),
    
    # Algorithms
    "binary_search": ConceptDefinition(
        name="Binary Search",
        description="An efficient search algorithm that finds an item in a sorted array by repeatedly dividing the search interval in half",
        key_terms=["sorted", "divide", "conquer", "middle", "logarithmic", "comparison", "interval", "half"],
        prerequisites=["arrays", "sorting", "recursion"],
        applications=["searching databases", "finding elements", "optimization problems"],
        common_misconceptions=[
            "trying to use on unsorted data",
            "off-by-one errors in implementation",
            "not understanding why it's O(log n)"
        ],
        difficulty_level=2
    ),
    
    "quicksort": ConceptDefinition(
        name="Quicksort",
        description="A divide-and-conquer sorting algorithm that picks a pivot element and partitions the array around it",
        key_terms=["pivot", "partition", "divide", "conquer", "recursive", "in-place", "comparison", "swap"],
        prerequisites=["recursion", "arrays", "partitioning"],
        applications=["general sorting", "data preprocessing", "database operations"],
        common_misconceptions=[
            "thinking it's always O(n log n)",
            "not understanding pivot selection importance",
            "confusing with merge sort"
        ],
        difficulty_level=4
    ),
    
    "dijkstra_algorithm": ConceptDefinition(
        name="Dijkstra's Algorithm",
        description="A graph algorithm that finds the shortest path between nodes in a weighted graph with non-negative edge weights",
        key_terms=["shortest path", "weighted graph", "priority queue", "relaxation", "distance", "vertex", "edge", "greedy"],
        prerequisites=["graphs", "priority_queue", "greedy_algorithms"],
        applications=["GPS navigation", "network routing", "social networks", "game pathfinding"],
        common_misconceptions=[
            "using with negative weights",
            "not understanding greedy choice",
            "confusing with A* algorithm"
        ],
        difficulty_level=4
    ),
    
    # Operating Systems
    "process_scheduling": ConceptDefinition(
        name="Process Scheduling",
        description="The method by which the operating system decides which process runs at any given time",
        key_terms=["process", "scheduler", "CPU", "time slice", "priority", "queue", "context switch", "preemptive", "non-preemptive"],
        prerequisites=["processes", "operating_system_basics"],
        applications=["multitasking", "server management", "real-time systems"],
        common_misconceptions=[
            "thinking all scheduling is round-robin",
            "not understanding context switching overhead",
            "confusing process with thread scheduling"
        ],
        difficulty_level=3
    ),
    
    "deadlock": ConceptDefinition(
        name="Deadlock",
        description="A situation where two or more processes are unable to proceed because each is waiting for the other to release resources",
        key_terms=["mutual exclusion", "hold and wait", "no preemption", "circular wait", "resource", "lock", "prevention", "avoidance"],
        prerequisites=["processes", "synchronization", "resources"],
        applications=["database systems", "operating systems", "concurrent programming"],
        common_misconceptions=[
            "thinking deadlock is the same as starvation",
            "not understanding all four conditions",
            "confusing prevention with avoidance"
        ],
        difficulty_level=4
    ),
    
    # Networks
    "tcp_ip": ConceptDefinition(
        name="TCP/IP Protocol",
        description="A suite of communication protocols used to interconnect network devices on the internet",
        key_terms=["transmission control protocol", "internet protocol", "packet", "reliable", "connection-oriented", "handshake", "acknowledgment", "flow control"],
        prerequisites=["networking_basics", "osi_model"],
        applications=["web browsing", "email", "file transfer", "remote access"],
        common_misconceptions=[
            "thinking TCP and IP are the same thing",
            "not understanding the layered approach",
            "confusing with UDP"
        ],
        difficulty_level=3
    ),
    
    # Databases
    "acid_properties": ConceptDefinition(
        name="ACID Properties",
        description="A set of properties that guarantee database transactions are processed reliably",
        key_terms=["atomicity", "consistency", "isolation", "durability", "transaction", "commit", "rollback", "concurrent"],
        prerequisites=["databases", "transactions"],
        applications=["banking systems", "e-commerce", "data integrity", "concurrent access"],
        common_misconceptions=[
            "thinking ACID is optional",
            "not understanding isolation levels",
            "confusing with BASE properties"
        ],
        difficulty_level=3
    )
}

# Concept relationships and dependencies
CONCEPT_DEPENDENCIES = {
    "binary_search_tree": ["binary_tree", "recursion", "tree_traversal"],
    "binary_search": ["arrays", "sorting", "recursion"],
    "quicksort": ["recursion", "arrays", "binary_search"],
    "dijkstra_algorithm": ["graphs", "priority_queue", "greedy_algorithms", "binary_search_tree"],
    "hash_table": ["arrays", "linked_list"],
    "deadlock": ["process_scheduling", "synchronization"],
    "tcp_ip": ["networking_basics", "osi_model"],
    "acid_properties": ["databases", "transactions"]
}

def get_concept_by_name(name: str) -> ConceptDefinition:
    """Get concept definition by name"""
    return CS_CONCEPTS.get(name.lower().replace(" ", "_").replace("-", "_"))

def find_related_concepts(concept_name: str) -> List[str]:
    """Find concepts related to the given concept"""
    concept_key = concept_name.lower().replace(" ", "_").replace("-", "_")
    related = []
    
    # Add prerequisites
    if concept_key in CONCEPT_DEPENDENCIES:
        related.extend(CONCEPT_DEPENDENCIES[concept_key])
    
    # Add concepts that depend on this one
    for concept, deps in CONCEPT_DEPENDENCIES.items():
        if concept_key in deps:
            related.append(concept)
    
    return list(set(related))

def get_concepts_by_subject(subject: str) -> List[str]:
    """Get all concepts for a given subject"""
    subject_mapping = {
        "data_structures": ["binary_search_tree", "linked_list", "hash_table"],
        "algorithms": ["binary_search", "quicksort", "dijkstra_algorithm"],
        "operating_systems": ["process_scheduling", "deadlock"],
        "computer_networks": ["tcp_ip"],
        "databases": ["acid_properties"]
    }
    return subject_mapping.get(subject, [])