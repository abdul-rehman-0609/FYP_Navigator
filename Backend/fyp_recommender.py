from typing import List, Optional
from student_profile import StudentProfile
from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine
from recommendation_engine import RecommendationEngine, Recommendation
from explanation_generator import ExplanationGenerator
from topic_tracker import TopicTracker
from ml_recommender import MLRecommender

class FYPRecommender:
    """
    Main system orchestrator for the FYP Topic Recommender.
    Integrates all components: Knowledge Base, Inference, Recommendation, Explanation, and Topic Tracking.
    """
    def __init__(self, csv_file: str = "selected_topics.csv", enable_ml_fallback: bool = True):
        # 1. Initialize Knowledge Base
        self.kb = KnowledgeBase()
        
        # 2. Initialize Inference Engine
        self.inference_engine = InferenceEngine()
        
        # 3. Initialize Topic Tracker
        self.topic_tracker = TopicTracker(csv_file)
        
        # 4. Initialize Recommendation Engine (with topic tracker)
        self.recommendation_engine = RecommendationEngine(self.kb, self.inference_engine, self.topic_tracker)
        
        # 5. Initialize Explanation Generator
        self.explanation_generator = ExplanationGenerator()
        
        # 6. Initialize ML Recommender (fallback for cold start)
        self.enable_ml_fallback = enable_ml_fallback
        self.ml_recommender = None
        if enable_ml_fallback:
            try:
                self.ml_recommender = MLRecommender(self.kb)
                print("✓ ML fallback system initialized")
            except Exception as e:
                print(f"⚠️  ML fallback disabled: {e}")
                self.enable_ml_fallback = False

    def get_recommendations_for_student(self, student: StudentProfile, top_n: int = 3, min_threshold: int = 3) -> str:
        """
        Full pipeline with ML fallback:
        1. Try knowledge-based system first
        2. If insufficient results (< min_threshold), activate ML fallback
        3. Generate human-readable explanation report
        
        Args:
            student: Student profile
            top_n: Target number of recommendations
            min_threshold: Minimum recommendations before ML fallback activates (default: 3)
        """
        # STEP 1: Try knowledge-based system
        kb_recommendations = self.recommendation_engine.generate_recommendations(student, top_n)
        
        ml_used = False
        all_recommendations = kb_recommendations
        
        # STEP 2: Check if we need ML fallback
        if len(kb_recommendations) < min_threshold and self.enable_ml_fallback and self.ml_recommender:
            ml_used = True
            needed = min_threshold - len(kb_recommendations)
            
            # Get unavailable topics
            unavailable_topics = self.topic_tracker.get_unavailable_topic_ids() if self.topic_tracker else []
            
            # Get ML recommendations
            try:
                ml_recommendations = self.ml_recommender.get_recommendations(
                    student, 
                    top_n=needed,
                    unavailable_topic_ids=unavailable_topics
                )
                
                # Combine: KB first (higher priority), then ML
                all_recommendations = kb_recommendations + ml_recommendations
                
                print(f"ℹ️  ML fallback activated: {len(kb_recommendations)} KB + {len(ml_recommendations)} ML = {len(all_recommendations)} total")
            except Exception as e:
                print(f"⚠️  ML fallback failed: {e}")
                # Continue with KB recommendations only
        
        # STEP 3: Check if we still have nothing
        if not all_recommendations:
            return f"No suitable topics found for {student.name}. Please broaden your interests or acquire more skills."

        # STEP 4: Generate report with ML indicator
        report = self.explanation_generator.generate_report(student, all_recommendations, ml_used=ml_used)
        return report

    def get_raw_recommendations(self, student: StudentProfile, top_n: int = 3, min_threshold: int = 3) -> List[Recommendation]:
        """Returns the raw recommendation objects for programmatic use."""
        # 1. KB Recommendations
        recommendations = self.recommendation_engine.generate_recommendations(student, top_n)
        
        # 2. ML Fallback (Only acts to ensure min_threshold is met)
        if len(recommendations) < min_threshold and self.enable_ml_fallback and self.ml_recommender:
            needed = min_threshold - len(recommendations)
            unavailable = self.topic_tracker.get_unavailable_topic_ids() if self.topic_tracker else []
            try:
                ml_recs = self.ml_recommender.get_recommendations(
                    student, 
                    top_n=needed, 
                    unavailable_topic_ids=unavailable
                )
                recommendations.extend(ml_recs)
                print(f"Added {len(ml_recs)} ML recommendations to meet threshold of {min_threshold}")
            except Exception as e:
                print(f"ML Fallback failed: {e}")

        # 3. Enrich with explanations if missing
        for rec in recommendations:
            if not rec.explanation:
                # Construct a brief explanation from match reasons
                if rec.match_reasons:
                    rec.explanation = " ".join(rec.match_reasons[:2])
                    if not rec.explanation.endswith('.'):
                        rec.explanation += "."
                else:
                    rec.explanation = "Recommended based on your profile compatibility."

        return recommendations
    
    def select_topic(self, student: StudentProfile, topic_id: str, score: float) -> bool:
        """
        Save a student's topic selection to the tracking system.
        
        Args:
            student: StudentProfile object
            topic_id: ID of the selected topic
            score: Recommendation score for the topic
            
        Returns:
            True if selection was saved successfully, False otherwise
        """
        # Get the topic details
        topic = self.kb.topics.get(topic_id)
        if not topic:
            print(f"Error: Topic {topic_id} not found in knowledge base.")
            return False
        
        # Save the selection
        success = self.topic_tracker.save_selection(
            student_id=student.student_id,
            student_name=student.name,
            topic_id=topic_id,
            topic_title=topic.title,
            score=score
        )
        
        if success:
            print(f"✓ Topic '{topic.title}' successfully selected for {student.name}")
        else:
            print(f"✗ Failed to select topic '{topic.title}' (may already be taken)")
        
        return success
    
    def display_all_selections(self) -> str:
        """Display all topic selections from the tracking system."""
        return self.topic_tracker.display_all_selections()
    
    def clear_all_selections(self) -> None:
        """Clear all topic selections (useful for testing/resetting)."""
        self.topic_tracker.clear_all_selections()
