from typing import List
from recommendation_engine import Recommendation
from student_profile import StudentProfile

class ExplanationGenerator:
    """
    Generates human-readable explanations for recommendations.
    """
    
    def generate_report(self, student: StudentProfile, recommendations: List[Recommendation], ml_used: bool = False) -> str:
        report = []
        report.append(f"FYP Recommendation Report for {student.name}")
        report.append("=" * 60)
        report.append(f"Major: {student.major} | CGPA: {student.cgpa}")
        report.append(f"Interests: {', '.join(student.preferred_domains)}")
        
        # ML Fallback Notice
        if ml_used:
            report.append("\n" + "⚠" * 60)
            report.append("ℹ️  ML FALLBACK ACTIVATED")
            report.append("Some recommendations use relaxed constraints to ensure you have options.")
            report.append("Consider improving your skills/CGPA for better knowledge-based matches.")
            report.append("⚠" * 60)
        
        report.append(f"\n{len(recommendations)} Top Recommendations based on your profile:\n")

        for i, rec in enumerate(recommendations):
            report.append(f"{'='*60}")
            report.append(f"RANK #{i+1}: {rec.topic.title}")
            report.append(f"{'='*60}")
            report.append(f"📊 MATCH SCORE: {rec.score:.2f}/100  |  Topic ID: {rec.topic.id}")
            report.append(f"Domain: {rec.topic.domain}  |  Difficulty: {rec.topic.difficulty}")
            report.append(f"\nDescription: {rec.topic.description}")
            
            report.append("\n✓ Why this matches you:")
            for reason in rec.match_reasons:
                report.append(f"  • {reason}")
            
            if rec.risk_level != "Low":
                report.append(f"\n⚠ Risk Assessment: {rec.risk_level.upper()}")
                for risk in rec.risk_reasons:
                    report.append(f"  • {risk}")
            else:
                 report.append(f"\n✓ Risk Assessment: {rec.risk_level} - Good fit!")

            report.append(f"\n🔧 Technical Feasibility: {int(rec.feasibility_score * 100)}%")
            report.append("")

        return "\n".join(report)
