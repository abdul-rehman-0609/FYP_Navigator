"""
Flask REST API Server for FYP Recommender System
Provides endpoints for the React frontend to interact with the backend.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, List, Optional
from datetime import datetime
import uuid

from student_profile import StudentProfile, Proficiency, InterestLevel
from fyp_recommender import FYPRecommender
from storage_manager import StorageManager
from knowledge_base import KnowledgeBase

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
storage = StorageManager()
recommender = FYPRecommender(enable_ml_fallback=True)
kb = KnowledgeBase()

# ==================== Helper Functions ====================

def frontend_to_backend_student(data: dict) -> StudentProfile:
    """Convert frontend student format to backend StudentProfile."""
    student = StudentProfile(
        student_id=data['id'],
        name=data['name'],
        cgpa=data['cgpa'],
        major=data['major'],
        year=data['year'],
        max_weekly_hours=data.get('preferences', {}).get('max_weekly_hours', 20),
        team_size_preference=data.get('preferences', {}).get('team_size', 1)
    )
    
    # Convert skills array to dict
    for skill in data.get('skills', []):
        proficiency = Proficiency[skill['proficiency']]
        student.add_skill(skill['name'], proficiency)
    
    # Convert interests array to dict
    for interest in data.get('interests', []):
        level = InterestLevel[interest['level']]
        student.add_interest(interest['domain'], level)
    
    # Add preferred domains from preferences
    student.preferred_domains = data.get('preferences', {}).get('preferred_domains', [])
    
    # Add completed courses
    student.completed_courses = set(data.get('completed_courses', []))
    
    return student


def backend_to_frontend_student(student: StudentProfile) -> dict:
    """Convert backend StudentProfile to frontend format."""
    return {
        'id': student.student_id,
        'name': student.name,
        'cgpa': student.cgpa,
        'major': student.major,
        'year': student.year,
        'skills': [
            {'name': name, 'proficiency': level.name}
            for name, level in student.skills.items()
        ],
        'interests': [
            {'domain': domain, 'level': level.name}
            for domain, level in student.interests.items()
        ],
        'completed_courses': list(student.completed_courses),
        'preferences': {
            'max_weekly_hours': student.max_weekly_hours,
            'team_size': student.team_size_preference,
            'preferred_domains': student.preferred_domains
        }
    }


def recommendation_to_frontend(rec, topic) -> dict:
    """Convert backend Recommendation to frontend format."""
    return {
        'topic_id': topic.id,
        'title': topic.title,
        'description': topic.description,
        'match_score': rec.score / 100.0,  # Normalize to 0-1 for frontend
        'required_skills': list(topic.requirements.required_skills.keys()),
        'required_courses': list(topic.requirements.required_courses),
        'explanation': rec.explanation,
        'domain': topic.domain,
        # Extended details
        'feasibility_score': rec.feasibility_score,
        'risk_level': rec.risk_level,
        'match_reasons': rec.match_reasons,
        'risk_reasons': rec.risk_reasons
    }


# ==================== Student Endpoints ====================

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students."""
    try:
        students = storage.load_all_students()
        return jsonify([backend_to_frontend_student(s) for s in students.values()])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """Get a single student by ID."""
    try:
        student = storage.load_student(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        return jsonify(backend_to_frontend_student(student))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students', methods=['POST'])
def create_student():
    """Create a new student."""
    try:
        data = request.json
        
        # Check if student already exists
        if storage.student_exists(data['id']):
            return jsonify({'error': 'Student ID already exists'}), 400
        
        # Convert and save
        student = frontend_to_backend_student(data)
        storage.save_student(student)
        
        return jsonify(backend_to_frontend_student(student)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    """Update an existing student."""
    try:
        data = request.json
        
        # Check if student exists
        if not storage.student_exists(student_id):
            return jsonify({'error': 'Student not found'}), 404
        
        # Convert and save
        data['id'] = student_id  # Ensure ID matches
        student = frontend_to_backend_student(data)
        storage.save_student(student)
        
        return jsonify(backend_to_frontend_student(student))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student."""
    try:
        if not storage.delete_student(student_id):
            return jsonify({'error': 'Student not found'}), 404
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Recommendation Endpoints ====================

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Generate recommendations for a student."""
    try:
        data = request.json
        student_id = data.get('student_id')
        count = data.get('count', 5)
        
        # Load student
        student = storage.load_student(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Generate recommendations
        recommendations = recommender.get_raw_recommendations(student, top_n=count)
        
        # Convert to frontend format
        frontend_recs = []
        for rec in recommendations:
            # rec.topic is already the TopicTemplate object
            frontend_recs.append(recommendation_to_frontend(rec, rec.topic))
        
        return jsonify(frontend_recs)
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/select_topic', methods=['POST'])
def select_topic():
    """Select a topic for a student."""
    try:
        data = request.json
        student_id = data.get('student_id')
        topic_id = data.get('topic_id')
        score = data.get('score', 0)
        
        student = storage.load_student(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
            
        success = recommender.select_topic(student, topic_id, score)
        if success:
            return jsonify({'message': 'Topic selected successfully'}), 200
        else:
            return jsonify({'error': 'Topic selection failed (already taken or invalid)'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== History Endpoints ====================

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get recommendation history, optionally filtered by student."""
    try:
        student_id = request.args.get('student_id')
        history = storage.load_recommendation_history(student_id)
        
        # Convert to frontend format
        frontend_history = []
        for entry in history:
            frontend_history.append({
                'id': str(uuid.uuid4()),  # Generate unique ID for frontend
                'student_id': entry['student_id'],
                'student_name': entry['student_name'],
                'timestamp': entry['timestamp'],
                'recommendations': entry['recommendations']
            })
        
        return jsonify(frontend_history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['POST'])
def save_to_history():
    """Save recommendations to history."""
    try:
        data = request.json
        student_id = data.get('student_id')
        recommendations = data.get('recommendations', [])
        
        # Get student name
        student = storage.load_student(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Save to history
        storage.save_recommendation(
            student_id=student_id,
            student_name=student.name,
            recommendations=recommendations,
            ml_used=False  # Could be enhanced to track this
        )
        
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear all recommendation history."""
    try:
        storage.clear_history()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Metadata Endpoints ====================

@app.route('/api/options', methods=['GET'])
def get_options():
    """Get dropdown options for the frontend."""
    try:
        # Aggregate all unique skills and courses from Knowledge Base
        all_skills = set()
        all_courses = set()
        
        # From domains
        for d in kb.domains.values():
            all_skills.update(d.base_skills.keys())
            all_courses.update(d.base_courses)
            
        # From techniques
        for t in kb.techniques.values():
            all_skills.update(t.required_skills.keys())
            
        # From contexts
        for c in kb.contexts.values():
            all_skills.update(c.additional_skills.keys())
            all_courses.update(c.additional_courses)
            
        return jsonify({
            'skills': sorted(list(all_skills)),
            'courses': sorted(list(all_courses)),
            'domains': sorted(list(kb.domains.keys())),
            'majors': [
                'Computer Science',
                'Software Engineering',
                'Information Technology',
                'Data Science',
                'Cybersecurity'
            ],
            'proficiency_levels': ['NOVICE', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'],
            'interest_levels': ['LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']
        })
    except Exception as e:
        print(f"Error fetching options: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics."""
    try:
        students = storage.load_all_students()
        history = storage.load_recommendation_history()
        
        # Count total recommendations
        total_recommendations = sum(
            len(entry.get('recommendations', []))
            for entry in history
        )
        
        return jsonify({
            'students': len(students),
            'recommendations': total_recommendations,
            'topics': len(kb.topics)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ml_enabled': recommender.enable_ml_fallback
    })


# ==================== Main ====================

if __name__ == '__main__':
    print("=" * 60)
    print("FYP Recommender System - API Server")
    print("=" * 60)
    print(f"Frontend URL: http://localhost:8080")
    print(f"Backend API: http://localhost:5000/api")
    print(f"ML Fallback: {'Enabled' if recommender.enable_ml_fallback else 'Disabled'}")
    print("=" * 60)
    print("\nStarting server...\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
