from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from enum import Enum, auto

class Proficiency(Enum):
    NOVICE = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

class InterestLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

@dataclass
class Skill:
    name: str
    level: Proficiency

@dataclass
class Interest:
    domain: str
    level: InterestLevel

@dataclass
class StudentProfile:
    """
    Represents a student's academic profile, skills, and preferences.
    """
    student_id: str
    name: str
    cgpa: float
    major: str
    year: int
    
    # Technical capabilities
    skills: Dict[str, Proficiency] = field(default_factory=dict)
    
    # Preferences
    interests: Dict[str, InterestLevel] = field(default_factory=dict)
    preferred_domains: List[str] = field(default_factory=list)
    
    # Constraints
    max_weekly_hours: int = 20
    team_size_preference: int = 1  # 1 for individual, >1 for group
    
    # History
    completed_courses: Set[str] = field(default_factory=set)

    def add_skill(self, name: str, level: Proficiency):
        self.skills[name.lower()] = level

    def add_interest(self, domain: str, level: InterestLevel):
        self.interests[domain.lower()] = level
        if level in [InterestLevel.HIGH, InterestLevel.VERY_HIGH] and domain.lower() not in self.preferred_domains:
            self.preferred_domains.append(domain.lower())

    def has_skill(self, skill_name: str, min_level: Proficiency = Proficiency.NOVICE) -> bool:
        skill_key = skill_name.lower()
        if skill_key not in self.skills:
            return False
        return self.skills[skill_key].value >= min_level.value

    def get_skill_level(self, skill_name: str) -> Proficiency:
        return self.skills.get(skill_name.lower(), Proficiency.NOVICE)
