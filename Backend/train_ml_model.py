"""
Training script for the ML-based recommender system.
Run this script to train and save the content-based filtering model.

Usage:
    python train_ml_model.py
"""

from knowledge_base import KnowledgeBase
from ml_recommender import MLRecommender
from student_profile import StudentProfile, Proficiency, InterestLevel
import os


def main():
    print("="*70)
    print("ML MODEL TRAINING SCRIPT")
    print("="*70)
    print()
    
    # Step 1: Load Knowledge Base
    print("Step 1: Loading Knowledge Base...")
    kb = KnowledgeBase()
    topic_count = kb.get_total_topic_count()
    print(f"✓ Loaded {topic_count} topics from knowledge base")
    print()
    
    # Step 2: Initialize ML Recommender
    print("Step 2: Initializing ML Recommender...")
    ml_recommender = MLRecommender(kb)
    print()
    
    # Step 3: Train the model
    print("Step 3: Training content-based filtering model...")
    print("   - Building TF-IDF vectorizer")
    print("   - Extracting topic features")
    print("   - Computing topic vectors")
    ml_recommender.fit()
    print()
    
    # Step 4: Save the model
    print("Step 4: Saving trained model...")
    model_path = "models/ml_model.pkl"
    ml_recommender.save_model(model_path)
    print()
    
    # Step 5: Validate with sample student
    print("Step 5: Validating model with sample student...")
    print("-" * 70)
    
    # Create a challenging student profile (cold start scenario)
    test_student = StudentProfile(
        student_id="TEST001",
        name="Test Student (Cold Start)",
        cgpa=2.0,  # Very low CGPA
        major="Computer Science",
        year=4,
        max_weekly_hours=10
    )
    test_student.add_skill("Python", Proficiency.NOVICE)
    test_student.add_interest("Web Development", InterestLevel.MEDIUM)
    
    print(f"Test Student Profile:")
    print(f"  Name: {test_student.name}")
    print(f"  CGPA: {test_student.cgpa}")
    print(f"  Skills: {list(test_student.skills.keys())}")
    print(f"  Interests: {list(test_student.interests.keys())}")
    print()
    
    # Get ML recommendations
    print("Generating ML recommendations...")
    recommendations = ml_recommender.get_recommendations(test_student, top_n=5)
    
    if recommendations:
        print(f"✓ Successfully generated {len(recommendations)} recommendations")
        print()
        print("Sample Recommendations:")
        print("-" * 70)
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"{i}. {rec.topic.title}")
            print(f"   Score: {rec.score:.2f} | Feasibility: {rec.feasibility_score:.2%}")
            print(f"   Domain: {rec.topic.domain} | Difficulty: {rec.topic.difficulty}")
            print()
    else:
        print("⚠️  No recommendations generated (this may indicate an issue)")
    
    print("="*70)
    print("TRAINING COMPLETE!")
    print("="*70)
    print()
    print(f"Model saved to: {os.path.abspath(model_path)}")
    print()
    print("Next steps:")
    print("  1. The ML model is now ready to use")
    print("  2. Run 'python demo.py' or 'python interactive_demo.py' to test")
    print("  3. The hybrid system will automatically use ML fallback when needed")
    print()
    print("To retrain the model:")
    print("  - Run this script again after updating the knowledge base")
    print("  - Or delete the model file and it will auto-train on first use")
    print("="*70)


if __name__ == "__main__":
    main()
