# FYP Recommender System - Enhanced with Topic Tracking

A Knowledge-Based Recommender System for Final Year Project (FYP) topics with CSV-based tracking to prevent topic overlap.

## Features

✅ **Multiple Topic Recommendations** - Get 5+ recommendations with detailed scores  
✅ **CSV-Based Tracking** - Automatically tracks selected topics to prevent overlaps  
✅ **Score Display** - Clear visibility of match scores for each recommendation  
✅ **Interactive Mode** - Create custom student profiles and test the system  
✅ **Automatic Filtering** - Selected topics are excluded from future recommendations  
✅ **ML Cold Start Solution** - Machine learning fallback ensures all students get recommendations  
✅ **Hybrid Recommender** - Combines knowledge-based and ML-based approaches  

## Quick Start

### Option 1: Run the Automated Demo
```bash
python demo.py
```
This runs a pre-configured demo with 3 sample students (Alice, Bob, and Charlie). The CSV file is automatically cleared at the start for a fresh run.

### Option 2: Interactive Mode (Recommended for Testing)
```bash
python interactive_demo.py
```
This allows you to:
- Create custom student profiles with your own data
- Specify skills, interests, and courses
- Get recommendations tailored to your inputs
- Select topics and see the CSV tracking in action

## Interactive Demo Menu

1. **Create new student profile** - Build a student profile step-by-step
2. **Get recommendations** - View recommendations for any student
3. **Select a topic** - Save a topic selection to CSV
4. **View all selections** - See all selected topics
5. **Clear all selections** - Reset the CSV file
6. **Exit** - Close the application

## Understanding the Recommendations

Each recommendation shows:
- **📊 MATCH SCORE** - Overall compatibility (0-100)
- **Topic ID** - Unique identifier for selection
- **Domain & Difficulty** - Project category and complexity
- **Why this matches you** - Reasons for the recommendation
- **Risk Assessment** - Potential challenges
- **🔧 Technical Feasibility** - Skill match percentage

## CSV Tracking

The system creates `selected_topics.csv` with the following format:
```csv
student_id,student_name,topic_id,topic_title,score,selected_date
S001,Alice Smith,WEB001,E-Commerce Platform,100.00,2025-12-19 10:27:22
```

### Key Features:
- **Prevents Overlaps** - Once a topic is selected, it won't appear in other students' recommendations
- **Tracks History** - Maintains a record of who selected what and when
- **Automatic Updates** - No manual intervention needed

## Why Some Students Get Fewer Recommendations

The system uses **hard constraints** to filter out unsuitable topics:
- **Skill Requirements** - Student must have minimum proficiency in required skills
- **CGPA Requirements** - Minimum CGPA threshold must be met
- **Course Prerequisites** - Required courses must be completed

### ML Fallback System

If a student gets fewer than 3 recommendations from the knowledge-based system, the **ML fallback automatically activates**:

- **Relaxed Constraints**: CGPA requirements reduced by 0.5 points, skill levels reduced by 1 level
- **Content-Based Filtering**: Uses TF-IDF and cosine similarity to match student interests with topics
- **Clear Indication**: Reports show when ML fallback was used

This ensures **no student is left without recommendations**, solving the cold start problem!

**Solution**: Adjust the student profile (add more skills, increase proficiency levels, or add completed courses) to unlock more knowledge-based recommendations.

## Example: Creating a Student in Interactive Mode

```
Enter student name: John Doe
Enter major: Computer Science
Enter CGPA: 3.5
Enter max weekly hours: 20

Add skills:
  Skill name: Python
  Proficiency level: 3 (Advanced)
  
  Skill name: JavaScript
  Proficiency level: 2 (Intermediate)

Add interests:
  Interest area: Web Development
  Interest level: 4 (Very High)

Add completed courses:
  Courses: Database Systems, Web Engineering, Data Structures
```

## Available Topics in Knowledge Base

1. **WEB001** - E-Commerce Recommendation Platform (Intermediate)
2. **WEB002** - Real-time Collaborative Code Editor (Advanced)
3. **AI001** - Traffic Sign Recognition System (Intermediate)
4. **AI002** - Legal Document Summarizer (Advanced)
5. **MOB001** - University Campus Navigator (Intermediate)

## Programmatic Usage

```python
from fyp_recommender import FYPRecommender
from student_profile import StudentProfile, Proficiency, InterestLevel

# Initialize recommender
recommender = FYPRecommender()

# Create student profile
student = StudentProfile(
    student_id="S001",
    name="Alice Smith",
    cgpa=3.2,
    major="Computer Science",
    year=4,
    max_weekly_hours=20
)

# Add skills and interests
student.add_skill("Python", Proficiency.ADVANCED)
student.add_interest("Web Development", InterestLevel.VERY_HIGH)

# Get recommendations (top 5)
recommendations = recommender.get_raw_recommendations(student, top_n=5)

# Select a topic
if recommendations:
    top_rec = recommendations[0]
    recommender.select_topic(student, top_rec.topic.id, top_rec.score)

# View all selections
print(recommender.display_all_selections())

# Clear selections (for testing)
recommender.clear_all_selections()
```

## Files Overview

### Core System
- **`demo.py`** - Automated demo with pre-configured students
- **`interactive_demo.py`** - Interactive mode with user input
- **`fyp_recommender.py`** - Main recommender system orchestrator with hybrid logic
- **`topic_tracker.py`** - CSV-based topic tracking module
- **`recommendation_engine.py`** - Knowledge-based scoring and ranking logic
- **`knowledge_base.py`** - Topic definitions and requirements
- **`inference_engine.py`** - Constraint checking and risk assessment
- **`explanation_generator.py`** - Report generation
- **`student_profile.py`** - Student profile data structure

### ML Module (New!)
- **`ml_recommender.py`** - ML-based recommender using content-based filtering
- **`train_ml_model.py`** - Model training script
- **`test_ml_integration.py`** - Test suite for ML integration
- **`models/ml_model.pkl`** - Trained TF-IDF model (auto-generated)

### Data Files
- **`selected_topics.csv`** - Topic selection tracking (auto-generated)

## Troubleshooting

**Q: Why am I getting "No suitable topics found"?**  
A: The student doesn't meet the minimum requirements for any available topics, even with ML fallback. Try:
- Increasing CGPA
- Adding more skills or increasing proficiency levels
- Adding completed courses
- Adding interests/preferred domains

**Q: Why are some topics not appearing?**  
A: They may have been selected by other students. Check `selected_topics.csv` or use the "View all selections" option.

**Q: How do I reset the system?**  
A: Use option 5 in interactive mode or call `recommender.clear_all_selections()` in code.

**Q: How do I retrain the ML model?**  
A: Run `python train_ml_model.py` after updating the knowledge base. The model trains in under 1 minute.

**Q: Can I disable ML fallback?**  
A: Yes! Initialize with `FYPRecommender(enable_ml_fallback=False)`

## License

This is an academic project for educational purposes.
