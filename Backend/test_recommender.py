import unittest
from student_profile import StudentProfile, Proficiency, InterestLevel
from knowledge_base import KnowledgeBase, TopicTemplate, TopicRequirement
from inference_engine import InferenceEngine
from recommendation_engine import RecommendationEngine
from fyp_recommender import FYPRecommender

class TestRecommenderSystem(unittest.TestCase):
    
    def setUp(self):
        self.recommender = FYPRecommender()
        self.kb = self.recommender.kb
        self.inference = self.recommender.inference_engine
        
        # Create a basic test user
        self.student = StudentProfile(
            student_id="T001",
            name="Test User",
            cgpa=3.0,
            major="CS",
            year=4
        )

    def test_student_profile_preferences(self):
        self.student.add_interest("Web Development", InterestLevel.VERY_HIGH)
        self.assertIn("web development", self.student.preferred_domains)
        self.assertEqual(self.student.interests["web development"], InterestLevel.VERY_HIGH)

    def test_hard_constraints_gpa(self):
        # Create a demanding topic
        t_req = TopicRequirement({}, 3.5, set(), 1, 3, 10)
        topic = TopicTemplate("T1", "Hard Topic", "Desc", "Test", "Hard", t_req, [], [])
        
        # Student has 3.0, needs 3.5
        passed, reasons = self.inference.check_hard_constraints(self.student, topic)
        self.assertFalse(passed)
        self.assertTrue(any("CGPA" in r for r in reasons))

    def test_hard_constraints_courses(self):
        t_req = TopicRequirement({}, 2.0, {"Advanced AI"}, 1, 3, 10)
        topic = TopicTemplate("T2", "AI Topic", "Desc", "AI", "Hard", t_req, [], [])
        
        passed, reasons = self.inference.check_hard_constraints(self.student, topic)
        self.assertFalse(passed)
        self.assertTrue(any("Missing required courses" in r for r in reasons))
        
        # Add course and retry
        self.student.completed_courses.add("Advanced AI")
        passed, reasons = self.inference.check_hard_constraints(self.student, topic)
        self.assertTrue(passed)

    def test_recommendation_scoring(self):
        # Add profile matching Web Dev
        self.student.add_skill("Python", Proficiency.INTERMEDIATE)
        self.student.add_interest("Web Development", InterestLevel.HIGH)
        self.student.completed_courses.update(["Database Systems", "Web Engineering"])
        
        recs = self.recommender.get_raw_recommendations(self.student)
        
        # Should find at least one recommendation
        self.assertTrue(len(recs) > 0)
        
        # The top recommendation should likely be related to Web Development
        # (Assuming the KB has web topics that fit)
        top_rec = recs[0]
        self.assertTrue(top_rec.score > 0)

    def test_full_pipeline_output(self):
        self.student.add_skill("Python", Proficiency.INTERMEDIATE)
        self.student.completed_courses.update(["Database Systems"])
        output = self.recommender.get_recommendations_for_student(self.student)
        self.assertIsInstance(output, str)
        self.assertTrue(len(output) > 10)

if __name__ == '__main__':
    unittest.main()
