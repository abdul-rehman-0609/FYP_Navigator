"""
Data Extractor Module
Extracts all possible dropdown values from the knowledge base for GUI consistency.
"""

from typing import List, Set, Dict
from knowledge_base import KnowledgeBase
from student_profile import Proficiency, InterestLevel


class DataExtractor:
    """Extracts and caches all possible values for GUI dropdowns."""
    
    def __init__(self):
        self.kb = KnowledgeBase()
        self._all_skills: Set[str] = set()
        self._all_courses: Set[str] = set()
        self._extract_data()
    
    def _extract_data(self):
        """Extract all unique skills and courses from knowledge base."""
        # Extract from domains
        for domain in self.kb.domains.values():
            self._all_skills.update(domain.base_skills.keys())
            self._all_courses.update(domain.base_courses)
        
        # Extract from techniques
        for technique in self.kb.techniques.values():
            self._all_skills.update(technique.required_skills.keys())
        
        # Extract from contexts
        for context in self.kb.contexts.values():
            self._all_skills.update(context.additional_skills.keys())
            self._all_courses.update(context.additional_courses)
    
    def get_all_skills(self) -> List[str]:
        """Get sorted list of all unique skills."""
        return sorted(list(self._all_skills))
    
    def get_all_courses(self) -> List[str]:
        """Get sorted list of all unique courses."""
        return sorted(list(self._all_courses))
    
    def get_all_domains(self) -> List[str]:
        """Get sorted list of all domain names."""
        return sorted(list(self.kb.domains.keys()))
    
    def get_all_techniques(self) -> List[str]:
        """Get sorted list of all technique names."""
        return sorted(list(self.kb.techniques.keys()))
    
    def get_all_contexts(self) -> List[str]:
        """Get sorted list of all context names."""
        return sorted(list(self.kb.contexts.keys()))
    
    def get_proficiency_levels(self) -> List[str]:
        """Get list of proficiency level names."""
        return [p.name for p in Proficiency]
    
    def get_interest_levels(self) -> List[str]:
        """Get list of interest level names."""
        return [i.name for i in InterestLevel]
    
    def get_majors(self) -> List[str]:
        """Get common majors (can be extended)."""
        return sorted([
            "Computer Science",
            "Software Engineering",
            "Information Technology",
            "Data Science",
            "Artificial Intelligence",
            "Cybersecurity",
            "Computer Engineering"
        ])
    
    def get_years(self) -> List[int]:
        """Get valid academic years."""
        return [1, 2, 3, 4, 5]
    
    def print_summary(self):
        """Print summary of extracted data."""
        print("=" * 60)
        print("DATA EXTRACTOR SUMMARY")
        print("=" * 60)
        print(f"Total Skills: {len(self._all_skills)}")
        print(f"Total Courses: {len(self._all_courses)}")
        print(f"Total Domains: {len(self.kb.domains)}")
        print(f"Total Techniques: {len(self.kb.techniques)}")
        print(f"Total Contexts: {len(self.kb.contexts)}")
        print(f"Proficiency Levels: {len(self.get_proficiency_levels())}")
        print(f"Interest Levels: {len(self.get_interest_levels())}")
        print("=" * 60)


if __name__ == "__main__":
    # Test the data extractor
    extractor = DataExtractor()
    extractor.print_summary()
    
    print("\nSample Skills (first 10):")
    for skill in extractor.get_all_skills()[:10]:
        print(f"  - {skill}")
    
    print("\nSample Courses (first 10):")
    for course in extractor.get_all_courses()[:10]:
        print(f"  - {course}")
    
    print("\nAll Domains:")
    for domain in extractor.get_all_domains():
        print(f"  - {domain}")
