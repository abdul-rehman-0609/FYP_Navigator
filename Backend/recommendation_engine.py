from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from student_profile import StudentProfile
from knowledge_base import KnowledgeBase, TopicTemplate
from inference_engine import InferenceEngine
from topic_tracker import TopicTracker

@dataclass
class Recommendation:
    topic: TopicTemplate
    score: float
    rank: int
    feasibility_score: float
    risk_level: str
    match_reasons: List[str]
    risk_reasons: List[str]
    explanation: str = ""

class RecommendationEngine:
    """
    Orchestrates the recommendation process using scoring and ranking algorithms.
    Filters out topics that have already been selected by other students.
    """
    def __init__(self, kb: KnowledgeBase, inference: InferenceEngine, topic_tracker: Optional[TopicTracker] = None):
        self.kb = kb
        self.inference = inference
        self.topic_tracker = topic_tracker

    def generate_recommendations(self, student: StudentProfile, top_n: int = 3) -> List[Recommendation]:
        candidates = self.kb.get_all_topics()
        scored_candidates = []
        
        # Get list of unavailable topics (already selected by other students)
        unavailable_topics = []
        if self.topic_tracker:
            unavailable_topics = self.topic_tracker.get_unavailable_topic_ids()

        for topic in candidates:
            # 0. Check if topic is already selected by another student
            if topic.id in unavailable_topics:
                continue  # Skip already-selected topics
            
            # 1. Hard Filter
            passed_hard_constraints, failure_reasons = self.inference.check_hard_constraints(student, topic)
            if not passed_hard_constraints:
                continue # Skip impossible topics

            # 2. Score Calculation
            score = self._calculate_score(student, topic)
            
            # 3. Risk Assessment
            risk_level, risk_reasons = self.inference.assess_risk(student, topic)
            
            # 4. Feasibility
            feas_score, _ = self.inference.evaluate_technical_feasibility(student, topic)

            # Generate positive match reasons
            match_reasons = self._get_match_reasons(student, topic)

            scored_candidates.append({
                'topic': topic,
                'score': score,
                'feasibility': feas_score,
                'risk_level': risk_level,
                'risk_reasons': risk_reasons,
                'match_reasons': match_reasons
            })

        # Rank by score descending
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # Create Recommendation objects
        results = []
        for i, item in enumerate(scored_candidates[:top_n]):
            results.append(Recommendation(
                topic=item['topic'],
                score=item['score'],
                rank=i + 1,
                feasibility_score=item['feasibility'],
                risk_level=item['risk_level'],
                risk_reasons=item['risk_reasons'],
                match_reasons=item['match_reasons']
            ))
            
        return results

    def _calculate_score(self, student: StudentProfile, topic: TopicTemplate) -> float:
        """
        Weighted scoring function.
        Weights: Skills (40%), Interests (30%), Difficulty Match (20%), Domain Preference (10%)
        """
        # Skill Score
        feas_score, _ = self.inference.evaluate_technical_feasibility(student, topic)
        skill_component = feas_score * 40

        # Interest Score
        interest_score = 0
        if topic.domain.lower() in student.interests:
            level = student.interests[topic.domain.lower()]
            interest_score = (level.value / 4.0) * 100
        interest_component = interest_score * 0.30

        # Domain Preference Bonus
        domain_bonus = 0
        if topic.domain.lower() in student.preferred_domains:
            domain_bonus = 100
        domain_component = domain_bonus * 0.10

        # Difficulty Match (Heuristic)
        # If student GPA is high, they should match with Advanced/Intermediate
        difficulty_score = 50 # Default neutral
        if topic.difficulty == "Advanced":
            if student.cgpa >= 3.5: difficulty_score = 100
            elif student.cgpa >= 3.0: difficulty_score = 80
            else: difficulty_score = 20
        elif topic.difficulty == "Intermediate":
            if student.cgpa >= 2.5: difficulty_score = 100
            else: difficulty_score = 60
        difficulty_component = difficulty_score * 0.20

        total_score = skill_component + interest_component + domain_component + difficulty_component
        return total_score

    def _get_match_reasons(self, student: StudentProfile, topic: TopicTemplate) -> List[str]:
        reasons = []
        if topic.domain.lower() in student.preferred_domains:
            reasons.append(f"Matches your preferred domain: {topic.domain}")
        
        req_skills = topic.requirements.required_skills
        matched_skills = []
        for skill in req_skills:
            if student.has_skill(skill):
                matched_skills.append(skill)
        
        if matched_skills:
            reasons.append(f"You have required skills: {', '.join(matched_skills)}")
            
        return reasons
