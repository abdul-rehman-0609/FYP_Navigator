# FYP Recommender System - GUI Application

## Overview

A professional desktop application for managing student profiles and generating Final Year Project (FYP) recommendations using a hybrid knowledge-based and machine learning approach.

## Features

### 🎓 Student Profile Management
- **Add/Edit Students** with comprehensive profile information
- **Dropdown menus** for all fields ensuring data consistency
- **Persistent storage** - all data saved automatically to JSON files
- **Search and filter** functionality
- **View detailed profiles** with all skills, interests, and preferences

### 🎯 Smart Recommendations
- **Knowledge-based engine** using expert rules and constraints
- **ML fallback** for cold-start scenarios
- **Explainable recommendations** with detailed reasoning
- **Topic availability tracking** to prevent duplicates
- **Customizable** number of recommendations (1-10)

### 📊 History Tracking
- **Complete recommendation history** with timestamps
- **Filter by student** or view all
- **Export functionality** for data backup

## Installation

### Prerequisites
- Python 3.8 or higher
- All dependencies from the main project

### Required Packages
```bash
pip install tkinter  # Usually comes with Python
```

All other dependencies should already be installed from the main FYP Recommender project.

## Usage

### Launching the Application

```bash
python gui_app.py
```

### Workflow

#### 1. Adding a Student

1. Go to the **"Add/Edit Student"** tab
2. Fill in basic information:
   - Student ID (required)
   - Name (required)
   - CGPA (0.0 - 4.0)
   - Major (select from dropdown)
   - Year (1-5)

3. Add **Skills**:
   - Select skill from dropdown (62 available skills)
   - Choose proficiency level (NOVICE, INTERMEDIATE, ADVANCED, EXPERT)
   - Click "Add Skill"
   - Repeat for all skills

4. Add **Interests**:
   - Select interest domain from dropdown
   - Choose interest level (LOW, MEDIUM, HIGH, VERY_HIGH)
   - Click "Add Interest"

5. Add **Completed Courses**:
   - Select from dropdown (13 available courses)
   - Click "Add Course"

6. Set **Preferences**:
   - Max Weekly Hours (5-40)
   - Team Size Preference (1-5)
   - Add Preferred Domains

7. Click **"Save Student"**

#### 2. Viewing Students

1. Go to the **"View Students"** tab
2. Use the search box to filter students
3. Select a student and:
   - **View Details** - See complete profile
   - **Edit Student** - Load into form for editing
   - **Delete Student** - Remove from database

#### 3. Getting Recommendations

1. Go to the **"Get Recommendations"** tab
2. Select a student from the dropdown
3. Choose number of recommendations (1-10)
4. Click **"Generate"**
5. View recommendations with:
   - Topic titles and descriptions
   - Match scores
   - Detailed explanations
   - Required skills and courses
6. Click **"Save to History"** to record the recommendations

#### 4. Viewing History

1. Go to the **"History"** tab
2. View all past recommendations
3. Filter by specific student if needed
4. Clear history if desired

## Data Storage

All data is stored in the `data/` directory:

- **`data/students.json`** - Student profiles
- **`data/recommendations_history.json`** - Recommendation history
- **`data/selected_topics.csv`** - Topic selection tracking

### Backup Your Data

Use **File → Export All Data** to create a backup of all student profiles and history.

## Available Dropdown Options

### Skills (62 total)
Including: python, java, javascript, machine learning, deep learning, nlp, opencv, unity, docker, aws, blockchain, and many more.

### Courses (13 total)
- Artificial Intelligence
- Computer Graphics
- Computer Networks
- Data Structures
- Database Systems
- Distributed Systems
- Embedded Systems
- Ethics in Computing
- Information Security
- Linear Algebra
- Mobile Application Development
- Statistics
- Web Engineering

### Domains (8 total)
- Artificial Intelligence
- Cloud Computing
- Cybersecurity
- Data Science
- Game Development
- IoT
- Mobile Development
- Web Development

### Proficiency Levels
- NOVICE (1)
- INTERMEDIATE (2)
- ADVANCED (3)
- EXPERT (4)

### Interest Levels
- LOW (1)
- MEDIUM (2)
- HIGH (3)
- VERY_HIGH (4)

## Tips for Best Results

1. **Be Specific with Skills**: Add all relevant skills with accurate proficiency levels
2. **Set Interests**: Higher interest levels (HIGH, VERY_HIGH) get prioritized
3. **Complete Courses Matter**: They unlock more topic options
4. **CGPA Threshold**: Some advanced topics require minimum CGPA (2.5-3.2)
5. **Preferred Domains**: Help narrow down recommendations to areas of interest

## Troubleshooting

### GUI doesn't launch
- Ensure tkinter is installed: `python -m tkinter`
- Check Python version: `python --version` (should be 3.8+)

### No recommendations generated
- Check student has sufficient skills
- Verify CGPA meets minimum requirements
- Try lowering the number of requested recommendations
- ML fallback will activate if knowledge-based system finds too few matches

### Data not persisting
- Check `data/` directory exists and is writable
- Verify JSON files are not corrupted
- Use "Export All Data" to backup before troubleshooting

## Architecture

```
gui_app.py
├── data_extractor.py      # Extracts dropdown options from knowledge base
├── storage_manager.py     # Handles JSON persistence
└── fyp_recommender.py     # Main recommendation engine
    ├── knowledge_base.py
    ├── inference_engine.py
    ├── recommendation_engine.py
    ├── ml_recommender.py
    └── explanation_generator.py
```

## Future Enhancements

- [ ] Batch import students from CSV
- [ ] Advanced filtering and sorting in View Students
- [ ] Recommendation comparison view
- [ ] Export recommendations to PDF
- [ ] Dark mode theme
- [ ] Student progress tracking

## Support

For issues or questions about the FYP Recommender System, please refer to the main project documentation.

---

**Version**: 1.0  
**Last Updated**: December 2025
