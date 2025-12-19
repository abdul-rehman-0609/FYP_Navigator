"""
Storage Manager Module
Handles persistent storage of student profiles and recommendation history.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from student_profile import StudentProfile, Proficiency, InterestLevel


class StorageManager:
    """Manages persistent storage for student profiles and recommendations."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.students_file = os.path.join(data_dir, "students.json")
        self.history_file = os.path.join(data_dir, "recommendations_history.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        if not os.path.exists(self.students_file):
            self._save_json(self.students_file, {})
        if not os.path.exists(self.history_file):
            self._save_json(self.history_file, [])
    
    def _save_json(self, filepath: str, data):
        """Save data to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_json(self, filepath: str):
        """Load data from JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if filepath == self.students_file else []
    
    # ==================== Student Profile Management ====================
    
    def save_student(self, student: StudentProfile) -> bool:
        """Save or update a student profile."""
        try:
            students = self._load_json(self.students_file)
            students[student.student_id] = self._student_to_dict(student)
            self._save_json(self.students_file, students)
            return True
        except Exception as e:
            print(f"Error saving student: {e}")
            return False
    
    def load_student(self, student_id: str) -> Optional[StudentProfile]:
        """Load a student profile by ID."""
        students = self._load_json(self.students_file)
        if student_id in students:
            return self._dict_to_student(students[student_id])
        return None
    
    def load_all_students(self) -> Dict[str, StudentProfile]:
        """Load all student profiles."""
        students = self._load_json(self.students_file)
        return {sid: self._dict_to_student(data) for sid, data in students.items()}
    
    def delete_student(self, student_id: str) -> bool:
        """Delete a student profile."""
        try:
            students = self._load_json(self.students_file)
            if student_id in students:
                del students[student_id]
                self._save_json(self.students_file, students)
                return True
            return False
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False
    
    def student_exists(self, student_id: str) -> bool:
        """Check if a student profile exists."""
        students = self._load_json(self.students_file)
        return student_id in students
    
    def get_all_student_ids(self) -> List[str]:
        """Get list of all student IDs."""
        students = self._load_json(self.students_file)
        return sorted(list(students.keys()))
    
    # ==================== Recommendation History Management ====================
    
    def save_recommendation(self, student_id: str, student_name: str, 
                          recommendations: List[Dict], ml_used: bool = False) -> bool:
        """Save a recommendation to history."""
        try:
            history = self._load_json(self.history_file)
            
            entry = {
                "timestamp": datetime.now().isoformat(),
                "student_id": student_id,
                "student_name": student_name,
                "recommendations": recommendations,
                "ml_used": ml_used
            }
            
            history.append(entry)
            self._save_json(self.history_file, history)
            return True
        except Exception as e:
            print(f"Error saving recommendation: {e}")
            return False
    
    def load_recommendation_history(self, student_id: Optional[str] = None) -> List[Dict]:
        """Load recommendation history, optionally filtered by student ID."""
        history = self._load_json(self.history_file)
        
        if student_id:
            return [entry for entry in history if entry["student_id"] == student_id]
        return history
    
    def clear_history(self) -> bool:
        """Clear all recommendation history."""
        try:
            self._save_json(self.history_file, [])
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
    
    # ==================== Conversion Methods ====================
    
    def _student_to_dict(self, student: StudentProfile) -> Dict:
        """Convert StudentProfile to dictionary for JSON storage."""
        return {
            "student_id": student.student_id,
            "name": student.name,
            "cgpa": student.cgpa,
            "major": student.major,
            "year": student.year,
            "skills": {name: level.value for name, level in student.skills.items()},
            "interests": {name: level.value for name, level in student.interests.items()},
            "preferred_domains": student.preferred_domains,
            "max_weekly_hours": student.max_weekly_hours,
            "team_size_preference": student.team_size_preference,
            "completed_courses": list(student.completed_courses)
        }
    
    def _dict_to_student(self, data: Dict) -> StudentProfile:
        """Convert dictionary to StudentProfile object."""
        student = StudentProfile(
            student_id=data["student_id"],
            name=data["name"],
            cgpa=data["cgpa"],
            major=data["major"],
            year=data["year"],
            max_weekly_hours=data.get("max_weekly_hours", 20),
            team_size_preference=data.get("team_size_preference", 1)
        )
        
        # Add skills
        for skill_name, level_value in data.get("skills", {}).items():
            student.skills[skill_name] = Proficiency(level_value)
        
        # Add interests
        for interest_name, level_value in data.get("interests", {}).items():
            student.interests[interest_name] = InterestLevel(level_value)
        
        # Add preferred domains
        student.preferred_domains = data.get("preferred_domains", [])
        
        # Add completed courses
        student.completed_courses = set(data.get("completed_courses", []))
        
        return student
    
    # ==================== Utility Methods ====================
    
    def export_all_data(self, export_path: str) -> bool:
        """Export all data to a single JSON file."""
        try:
            all_data = {
                "students": self._load_json(self.students_file),
                "history": self._load_json(self.history_file),
                "export_date": datetime.now().isoformat()
            }
            self._save_json(export_path, all_data)
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get storage statistics."""
        students = self._load_json(self.students_file)
        history = self._load_json(self.history_file)
        
        return {
            "total_students": len(students),
            "total_recommendations": len(history),
            "storage_size_kb": (
                os.path.getsize(self.students_file) + 
                os.path.getsize(self.history_file)
            ) / 1024
        }


if __name__ == "__main__":
    # Test the storage manager
    sm = StorageManager()
    
    print("Storage Manager Test")
    print("=" * 60)
    
    # Create a test student
    test_student = StudentProfile(
        student_id="TEST001",
        name="Test Student",
        cgpa=3.5,
        major="Computer Science",
        year=4
    )
    test_student.add_skill("python", Proficiency.ADVANCED)
    test_student.add_interest("artificial intelligence", InterestLevel.VERY_HIGH)
    test_student.completed_courses.add("Data Structures")
    
    # Save student
    if sm.save_student(test_student):
        print("✓ Student saved successfully")
    
    # Load student
    loaded = sm.load_student("TEST001")
    if loaded:
        print(f"✓ Student loaded: {loaded.name}")
    
    # Get statistics
    stats = sm.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total Students: {stats['total_students']}")
    print(f"  Total Recommendations: {stats['total_recommendations']}")
    print(f"  Storage Size: {stats['storage_size_kb']:.2f} KB")
