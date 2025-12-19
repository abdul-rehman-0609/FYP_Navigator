"""
Test script for ML cold start integration.
Tests the hybrid recommender system with edge cases.
"""

from student_profile import StudentProfile, Proficiency, InterestLevel
from fyp_recommender import FYPRecommender


def test_cold_start_student():
    """Test a student with very low qualifications (cold start scenario)."""
    print("="*70)
    print("TEST 1: COLD START STUDENT (Low CGPA, Minimal Skills)")
    print("="*70)
    print()
    
    recommender = FYPRecommender()
    
    # Create a student who would normally get NO recommendations
    cold_start_student = StudentProfile(
        student_id="COLD001",
        name="Cold Start Student",
        cgpa=2.0,  # Very low
        major="Computer Science",
        year=4,
        max_weekly_hours=10
    )
    cold_start_student.add_skill("Python", Proficiency.NOVICE)
    cold_start_student.add_interest("Web Development", InterestLevel.MEDIUM)
    
    print(f"Student Profile:")
    print(f"  Name: {cold_start_student.name}")
    print(f"  CGPA: {cold_start_student.cgpa}")
    print(f"  Skills: {list(cold_start_student.skills.keys())}")
    print(f"  Interests: {list(cold_start_student.interests.keys())}")
    print(f"  Completed Courses: {len(cold_start_student.completed_courses)}")
    print()
    
    # Get recommendations
    report = recommender.get_recommendations_for_student(cold_start_student, top_n=5)
    print(report)
    print()


def test_normal_student():
    """Test a normal student who should get KB recommendations."""
    print("\n" + "="*70)
    print("TEST 2: NORMAL STUDENT (Good CGPA, Decent Skills)")
    print("="*70)
    print()
    
    recommender = FYPRecommender()
    
    # Create a normal student
    normal_student = StudentProfile(
        student_id="NORM001",
        name="Normal Student",
        cgpa=3.2,
        major="Computer Science",
        year=4,
        max_weekly_hours=20
    )
    normal_student.add_skill("Python", Proficiency.INTERMEDIATE)
    normal_student.add_skill("JavaScript", Proficiency.INTERMEDIATE)
    normal_student.add_skill("HTML", Proficiency.INTERMEDIATE)
    normal_student.add_skill("CSS", Proficiency.INTERMEDIATE)
    normal_student.add_interest("Web Development", InterestLevel.VERY_HIGH)
    normal_student.completed_courses.update(["Web Engineering", "Database Systems"])
    
    print(f"Student Profile:")
    print(f"  Name: {normal_student.name}")
    print(f"  CGPA: {normal_student.cgpa}")
    print(f"  Skills: {list(normal_student.skills.keys())}")
    print(f"  Interests: {list(normal_student.interests.keys())}")
    print(f"  Completed Courses: {list(normal_student.completed_courses)}")
    print()
    
    # Get recommendations
    report = recommender.get_recommendations_for_student(normal_student, top_n=5)
    print(report)
    print()


def test_borderline_student():
    """Test a borderline student (might get 1-2 KB recommendations)."""
    print("\n" + "="*70)
    print("TEST 3: BORDERLINE STUDENT (Moderate CGPA, Few Skills)")
    print("="*70)
    print()
    
    recommender = FYPRecommender()
    
    # Create a borderline student
    borderline_student = StudentProfile(
        student_id="BORDER001",
        name="Borderline Student",
        cgpa=2.6,
        major="Software Engineering",
        year=4,
        max_weekly_hours=15
    )
    borderline_student.add_skill("Python", Proficiency.NOVICE)
    borderline_student.add_skill("Java", Proficiency.NOVICE)
    borderline_student.add_interest("Mobile Development", InterestLevel.HIGH)
    borderline_student.completed_courses.update(["Introduction to Computing"])
    
    print(f"Student Profile:")
    print(f"  Name: {borderline_student.name}")
    print(f"  CGPA: {borderline_student.cgpa}")
    print(f"  Skills: {list(borderline_student.skills.keys())}")
    print(f"  Interests: {list(borderline_student.interests.keys())}")
    print(f"  Completed Courses: {list(borderline_student.completed_courses)}")
    print()
    
    # Get recommendations
    report = recommender.get_recommendations_for_student(borderline_student, top_n=5)
    print(report)
    print()


def test_ml_disabled():
    """Test with ML fallback disabled."""
    print("\n" + "="*70)
    print("TEST 4: ML FALLBACK DISABLED (Cold Start Student)")
    print("="*70)
    print()
    
    recommender = FYPRecommender(enable_ml_fallback=False)
    
    # Same cold start student
    cold_start_student = StudentProfile(
        student_id="COLD002",
        name="Cold Start Student (No ML)",
        cgpa=2.0,
        major="Computer Science",
        year=4,
        max_weekly_hours=10
    )
    cold_start_student.add_skill("Python", Proficiency.NOVICE)
    cold_start_student.add_interest("Web Development", InterestLevel.MEDIUM)
    
    print(f"Student Profile:")
    print(f"  Name: {cold_start_student.name}")
    print(f"  CGPA: {cold_start_student.cgpa}")
    print(f"  Skills: {list(cold_start_student.skills.keys())}")
    print()
    
    # Get recommendations (should fail without ML)
    report = recommender.get_recommendations_for_student(cold_start_student, top_n=5)
    print(report)
    print()


def main():
    print("\n" + "█"*70)
    print("ML COLD START INTEGRATION TEST SUITE")
    print("█"*70)
    print()
    print("This test suite validates the hybrid recommender system:")
    print("  ✓ Knowledge-based system for qualified students")
    print("  ✓ ML fallback for cold start scenarios")
    print("  ✓ Hybrid combination when KB returns insufficient results")
    print()
    
    try:
        # Run all tests
        test_normal_student()      # Should use KB only
        test_borderline_student()  # Might use hybrid
        test_cold_start_student()  # Should use ML fallback
        test_ml_disabled()         # Should fail gracefully
        
        print("\n" + "█"*70)
        print("ALL TESTS COMPLETED!")
        print("█"*70)
        print()
        print("Summary:")
        print("  ✓ Test 1 (Normal): Should show KB recommendations only")
        print("  ✓ Test 2 (Borderline): May show hybrid (KB + ML)")
        print("  ✓ Test 3 (Cold Start): Should show ML fallback notice")
        print("  ✓ Test 4 (ML Disabled): Should show 'No suitable topics' message")
        print()
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
