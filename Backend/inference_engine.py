from typing import List, Dict, Tuple
from student_profile import StudentProfile, Proficiency
from knowledge_base import TopicTemplate, TopicRequirement

class InferenceEngine:
    """
    Rule-based engine to check constraints and evaluate feasibility.
    """

    def check_hard_constraints(self, student: StudentProfile, topic: TopicTemplate) -> Tuple[bool, List[str]]:
        """
        Checks necessary conditions for a topic.
        Returns (passed, list of failure reasons).
        """
        reasons = []
        reqs = topic.requirements

        # 1. CGPA Requirement
        if student.cgpa < reqs.min_cgpa:
            reasons.append(f"CGPA {student.cgpa} is below minimum requirement {reqs.min_cgpa}")

        # 2. Prerequisite Courses
        missing_courses = reqs.required_courses - student.completed_courses
        if missing_courses:
            reasons.append(f"Missing required courses: {', '.join(missing_courses)}")

        # 3. Team Size Constraints
        if student.team_size_preference < reqs.team_size_min:
             reasons.append(f"Preferred team size {student.team_size_preference} is too small (min {reqs.team_size_min})")
        
        # 4. Time Availability
        if student.max_weekly_hours < reqs.estimated_weekly_hours:
             reasons.append(f"Available hours {student.max_weekly_hours} less than required {reqs.estimated_weekly_hours}")

        return (len(reasons) == 0, reasons)

    def evaluate_technical_feasibility(self, student: StudentProfile, topic: TopicTemplate) -> Tuple[float, List[str]]:
        """
        Calculates a feasibility score (0.0 - 1.0) based on skills.
        Returns (score, list of missing/weak skills).
        """
        req_skills = topic.requirements.required_skills
        if not req_skills:
            return 1.0, []

        total_weight = 0
        matched_weight = 0
        gaps = []

        for skill, min_level_val in req_skills.items():
            total_weight += min_level_val
            student_level = student.get_skill_level(skill)
            
            if student_level.value >= min_level_val:
                matched_weight += min_level_val
            else:
                # Partial credit? No, strict penalty for feasibility, but we track the gap
                # Let's give partial credit for being close
                matched_weight += student_level.value * 0.5
                gaps.append(f"Skill '{skill}' level {student_level.name} < required {Proficiency(min_level_val).name}")

        score = matched_weight / total_weight if total_weight > 0 else 1.0
        return score, gaps

    def assess_risk(self, student: StudentProfile, topic: TopicTemplate) -> Tuple[str, List[str]]:
        """
        Determines risk level: 'Low', 'Medium', 'High'.
        """
        risk_level = "Low"
        reasons = []

        # 1. Domain experience
        if topic.domain.lower() not in student.interests:
             reasons.append(f"No prior interest expressed in domain '{topic.domain}'")
             risk_level = "Medium"

        # 2. Complexity vs GPA check
        if topic.difficulty == "Advanced" and student.cgpa < 3.0:
            reasons.append("High difficulty topic with CGPA < 3.0")
            risk_level = "High"

        # 3. Technical Feasibility Check
        feasibility_score, skill_gaps = self.evaluate_technical_feasibility(student, topic)
        if feasibility_score < 0.6:
            risk_level = "High"
            reasons.extend(["Significant skill gaps:"] + skill_gaps)
        elif feasibility_score < 0.8:
            if risk_level == "Low": risk_level = "Medium"
            reasons.extend(["Moderate skill gaps:"] + skill_gaps)

        return risk_level, reasons
