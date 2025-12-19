from typing import List, Dict, Tuple
from dataclasses import dataclass
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

from student_profile import StudentProfile
from knowledge_base import KnowledgeBase, TopicTemplate
from recommendation_engine import Recommendation


@dataclass
class MLRecommendation:
    """ML-based recommendation with similarity score."""
    topic: TopicTemplate
    similarity_score: float
    feasibility_score: float
    final_score: float
    is_ml_recommendation: bool = True


class MLRecommender:
    """
    Machine Learning-based recommender using content-based filtering.
    Acts as a fallback when knowledge-based system returns insufficient results.
    Uses relaxed constraints to ensure all students get recommendations.
    """
    
    def __init__(self, kb: KnowledgeBase, model_path: str = "models/ml_model.pkl"):
        self.kb = kb
        self.model_path = model_path
        self.vectorizer = None
        self.topic_vectors = None
        self.topic_list = []
        self.is_trained = False
        
        # Try to load pre-trained model
        if os.path.exists(model_path):
            self.load_model(model_path)
        else:
            # If no model exists, train on the fly
            print(f"⚠️  No pre-trained model found at {model_path}")
            print("Training ML model on the fly...")
            self.fit()
    
    def fit(self):
        """
        Train the content-based filtering model using TF-IDF.
        Builds a vectorizer from all topics in the knowledge base.
        """
        self.topic_list = self.kb.get_all_topics()
        
        if not self.topic_list:
            raise ValueError("Knowledge base has no topics to train on!")
        
        # Create text documents from topics
        topic_documents = self._create_topic_documents(self.topic_list)
        
        # Build TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=1,
            max_df=0.8
        )
        
        # Fit and transform topics
        self.topic_vectors = self.vectorizer.fit_transform(topic_documents)
        self.is_trained = True
        
        print(f"✓ ML model trained on {len(self.topic_list)} topics")
        print(f"✓ Vocabulary size: {len(self.vectorizer.vocabulary_)}")
    
    def _create_topic_documents(self, topics: List[TopicTemplate]) -> List[str]:
        """
        Convert topics to text documents for TF-IDF vectorization.
        Combines title, description, domain, technique, context, and keywords.
        """
        documents = []
        for topic in topics:
            # Combine all textual features
            doc_parts = [
                topic.title,
                topic.description,
                topic.domain,
                topic.technique,
                topic.context,
                topic.difficulty,
                ' '.join(topic.keywords),
                ' '.join(topic.requirements.required_skills.keys()),
            ]
            
            # Join with spaces and clean
            document = ' '.join(doc_parts).lower()
            documents.append(document)
        
        return documents
    
    def _create_student_query(self, student: StudentProfile) -> str:
        """
        Convert student profile to a query document for similarity matching.
        """
        query_parts = []
        
        # Add interests (most important)
        for interest, level in student.interests.items():
            # Repeat interest based on level (higher level = more weight)
            query_parts.extend([interest] * level.value)
        
        # Add preferred domains
        query_parts.extend(student.preferred_domains)
        
        # Add skills
        for skill, proficiency in student.skills.items():
            # Repeat skill based on proficiency
            query_parts.extend([skill] * proficiency.value)
        
        # Add completed courses
        query_parts.extend(student.completed_courses)
        
        # Add major
        query_parts.append(student.major)
        
        return ' '.join(query_parts).lower()
    
    def _check_relaxed_constraints(self, student: StudentProfile, topic: TopicTemplate) -> Tuple[float, List[str]]:
        """
        Apply relaxed constraints for ML recommendations.
        Returns a feasibility score (0.0 to 1.0) instead of hard pass/fail.
        
        Relaxations:
        - CGPA: -0.3 points
        - Skills: -1 proficiency level
        - Courses: Optional (weighted)
        """
        score = 1.0
        reasons = []
        
        # 1. CGPA Check (Relaxed by 0.5 - more lenient for cold start)
        relaxed_cgpa = topic.requirements.min_cgpa - 0.5  # Increased from 0.3
        if student.cgpa < relaxed_cgpa:
            penalty = 0.3  # Reduced penalty (was 0.5)
            score *= penalty
            reasons.append(f"CGPA below relaxed threshold ({student.cgpa:.2f} < {relaxed_cgpa:.2f})")
        elif student.cgpa < topic.requirements.min_cgpa:
            penalty = 0.7  # Reduced penalty (was 0.8)
            score *= penalty
            reasons.append(f"CGPA slightly below requirement (relaxed from {topic.requirements.min_cgpa})")
        
        # 2. Skills Check (Relaxed by 1 level)
        skill_penalties = []
        for skill, min_level in topic.requirements.required_skills.items():
            relaxed_level = max(1, min_level - 1)  # Reduce by 1 level, minimum 1
            
            if not student.has_skill(skill):
                penalty = 0.5  # Reduced penalty (was 0.6)
                score *= penalty
                skill_penalties.append(f"Missing {skill} (can learn)")
            elif student.skills[skill].value < relaxed_level:
                penalty = 0.6  # Reduced penalty (was 0.7)
                score *= penalty
                skill_penalties.append(f"{skill} below relaxed level")
            elif student.skills[skill].value < min_level:
                penalty = 0.8  # Reduced penalty (was 0.9)
                score *= penalty
                skill_penalties.append(f"{skill} slightly below requirement")
        
        if skill_penalties:
            reasons.extend(skill_penalties[:2])  # Limit to top 2 skill issues
        
        # 3. Course Check (Made optional - weighted)
        if topic.requirements.required_courses:
            completed = student.completed_courses & topic.requirements.required_courses
            required = topic.requirements.required_courses
            match_ratio = len(completed) / len(required) if required else 1.0
            
            # Weight: 0.5 base + 0.5 * match_ratio
            course_weight = 0.5 + 0.5 * match_ratio
            score *= course_weight
            
            if match_ratio < 0.5:
                missing_courses = list(required - completed)[:2]
                reasons.append(f"Missing courses: {', '.join(missing_courses)}")
        
        # 4. Time availability check (soft)
        if student.max_weekly_hours < topic.requirements.estimated_weekly_hours:
            penalty = 0.9
            score *= penalty
            reasons.append(f"May need {topic.requirements.estimated_weekly_hours}h/week (you have {student.max_weekly_hours}h)")
        
        return score, reasons
    
    def get_recommendations(self, student: StudentProfile, top_n: int = 3, 
                          unavailable_topic_ids: List[str] = None) -> List[Recommendation]:
        """
        Generate ML-based recommendations using content-based filtering.
        
        Args:
            student: Student profile
            top_n: Number of recommendations to return
            unavailable_topic_ids: Topics already selected by others
        
        Returns:
            List of Recommendation objects with ML-based scoring
        """
        if not self.is_trained:
            raise RuntimeError("ML model not trained! Call fit() first or load a trained model.")
        
        unavailable_topic_ids = unavailable_topic_ids or []
        
        # Create student query
        student_query = self._create_student_query(student)
        
        # Vectorize student query
        student_vector = self.vectorizer.transform([student_query])
        
        # Calculate cosine similarity with all topics
        similarities = cosine_similarity(student_vector, self.topic_vectors)[0]
        
        # Create candidate list with scores
        candidates = []
        for idx, topic in enumerate(self.topic_list):
            # Skip unavailable topics
            if topic.id in unavailable_topic_ids:
                continue
            
            # Get similarity score
            similarity_score = similarities[idx]
            
            # Apply relaxed constraints
            feasibility_score, constraint_reasons = self._check_relaxed_constraints(student, topic)
            
            # Skip if feasibility is too low (even with relaxed constraints)
            # Very lenient threshold for cold start scenarios
            if feasibility_score < 0.01:  # Changed from 0.1 to 0.01 for cold start
                continue
            
            # Calculate final score (weighted combination)
            final_score = (0.6 * similarity_score * 100) + (0.4 * feasibility_score * 100)
            
            # Generate match reasons
            match_reasons = self._generate_ml_match_reasons(student, topic, similarity_score)
            
            # Combine with constraint reasons
            all_reasons = match_reasons + constraint_reasons
            
            candidates.append({
                'topic': topic,
                'similarity_score': similarity_score,
                'feasibility_score': feasibility_score,
                'final_score': final_score,
                'match_reasons': match_reasons,
                'risk_reasons': constraint_reasons
            })
        
        # Sort by final score
        candidates.sort(key=lambda x: x['final_score'], reverse=True)
        
        # Convert to Recommendation objects
        recommendations = []
        for i, candidate in enumerate(candidates[:top_n]):
            rec = Recommendation(
                topic=candidate['topic'],
                score=candidate['final_score'],
                rank=i + 1,
                feasibility_score=candidate['feasibility_score'],
                risk_level="Medium-High (ML Fallback)",  # Indicate ML recommendation
                match_reasons=candidate['match_reasons'],
                risk_reasons=candidate['risk_reasons']
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_ml_match_reasons(self, student: StudentProfile, topic: TopicTemplate, 
                                   similarity_score: float) -> List[str]:
        """Generate human-readable match reasons for ML recommendations."""
        reasons = []
        
        # Similarity-based reason
        if similarity_score > 0.3:
            reasons.append(f"High content similarity ({similarity_score:.2%}) with your profile")
        else:
            reasons.append(f"Moderate match ({similarity_score:.2%}) based on interests")
        
        # Interest match
        if topic.domain.lower() in student.interests:
            level = student.interests[topic.domain.lower()]
            reasons.append(f"Matches your {level.name.lower()} interest in {topic.domain}")
        
        # Skill overlap
        matched_skills = [skill for skill in topic.requirements.required_skills.keys() 
                         if student.has_skill(skill)]
        if matched_skills:
            reasons.append(f"You have some relevant skills: {', '.join(matched_skills[:3])}")
        
        # Domain preference
        if topic.domain.lower() in student.preferred_domains:
            reasons.append(f"Aligns with your preferred domain: {topic.domain}")
        
        return reasons[:3]  # Limit to top 3 reasons
    
    def save_model(self, path: str = None):
        """Save the trained model to disk."""
        if not self.is_trained:
            raise RuntimeError("Cannot save untrained model!")
        
        path = path or self.model_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save model components
        model_data = {
            'vectorizer': self.vectorizer,
            'topic_vectors': self.topic_vectors,
            'topic_list': self.topic_list
        }
        
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✓ ML model saved to {path}")
    
    def load_model(self, path: str):
        """Load a pre-trained model from disk."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vectorizer = model_data['vectorizer']
        self.topic_vectors = model_data['topic_vectors']
        self.topic_list = model_data['topic_list']
        self.is_trained = True
        
        print(f"✓ ML model loaded from {path}")
        print(f"✓ Model contains {len(self.topic_list)} topics")
