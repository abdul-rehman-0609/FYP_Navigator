"""
Test script to demonstrate dynamic topic generation.
Shows the variety and quantity of topics generated.
"""
from knowledge_base import KnowledgeBase

def main():
    print("="*70)
    print("DYNAMIC TOPIC GENERATION DEMONSTRATION")
    print("="*70)
    
    kb = KnowledgeBase()
    
    # Show statistics
    print(f"\n📊 Total Topics Generated: {kb.get_total_topic_count()}")
    print(f"📊 Domains: {len(kb.domains)}")
    print(f"📊 Techniques: {len(kb.techniques)}")
    print(f"📊 Contexts: {len(kb.contexts)}")
    
    # Show domain breakdown
    print(f"\n{'='*70}")
    print("TOPICS BY DOMAIN")
    print(f"{'='*70}")
    for domain_name in kb.domains.keys():
        count = len(kb.get_topics_by_domain(domain_name))
        print(f"  {domain_name}: {count} topics")
    
    # Show technique breakdown
    print(f"\n{'='*70}")
    print("TOPICS BY TECHNIQUE")
    print(f"{'='*70}")
    for technique_name in kb.techniques.keys():
        count = len(kb.get_topics_by_technique(technique_name))
        print(f"  {technique_name}: {count} topics")
    
    # Show sample topics from different domains
    print(f"\n{'='*70}")
    print("SAMPLE GENERATED TOPICS (First 10)")
    print(f"{'='*70}\n")
    
    all_topics = kb.get_all_topics()
    for i, topic in enumerate(all_topics[:10], 1):
        print(f"{i}. {topic.title}")
        print(f"   ID: {topic.id}")
        print(f"   Formula: {topic.domain} + {topic.technique} + {topic.context}")
        print(f"   Difficulty: {topic.difficulty} | CGPA: {topic.requirements.min_cgpa}")
        print(f"   Description: {topic.description}")
        print()
    
    # Show examples of different techniques
    print(f"{'='*70}")
    print("EXAMPLES: MACHINE LEARNING TOPICS")
    print(f"{'='*70}\n")
    
    ml_topics = kb.get_topics_by_technique("Machine Learning")[:5]
    for i, topic in enumerate(ml_topics, 1):
        print(f"{i}. {topic.title}")
        print(f"   Context: {topic.context} | Domain: {topic.domain}")
        print()
    
    # Show examples of different contexts
    print(f"{'='*70}")
    print("EXAMPLES: HEALTHCARE APPLICATION TOPICS")
    print(f"{'='*70}\n")
    
    healthcare_topics = kb.get_topics_by_context("Healthcare Application")[:5]
    for i, topic in enumerate(healthcare_topics, 1):
        print(f"{i}. {topic.title}")
        print(f"   Technique: {topic.technique} | Domain: {topic.domain}")
        print()

if __name__ == "__main__":
    main()
