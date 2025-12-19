import csv
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class TopicTracker:
    """
    Manages topic selections using CSV file storage.
    Prevents topic overlap by tracking which students have selected which topics.
    """
    def __init__(self, csv_file: str = "selected_topics.csv"):
        self.csv_file = csv_file
        self.fieldnames = ['student_id', 'student_name', 'topic_id', 'topic_title', 'score', 'selected_date']
        self._initialize_csv()
    
    def _initialize_csv(self):
        """Create CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
    
    def save_selection(self, student_id: str, student_name: str, topic_id: str, 
                      topic_title: str, score: float) -> bool:
        """
        Save a student's topic selection to the CSV file.
        
        Args:
            student_id: Student's unique identifier
            student_name: Student's name
            topic_id: Selected topic's ID
            topic_title: Selected topic's title
            score: Recommendation score for this topic
            
        Returns:
            True if saved successfully, False if topic already selected
        """
        # Check if topic is already selected
        if not self.is_topic_available(topic_id):
            return False
        
        # Check if student already has a selection
        existing = self.get_student_selection(student_id)
        if existing:
            print(f"Warning: Student {student_id} already selected topic {existing['topic_id']}")
            return False
        
        # Save the selection
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow({
                'student_id': student_id,
                'student_name': student_name,
                'topic_id': topic_id,
                'topic_title': topic_title,
                'score': f"{score:.2f}",
                'selected_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return True
    
    def is_topic_available(self, topic_id: str) -> bool:
        """
        Check if a topic is still available (not selected by another student).
        
        Args:
            topic_id: Topic ID to check
            
        Returns:
            True if available, False if already selected
        """
        selected_topics = self.get_selected_topics()
        return topic_id not in [t['topic_id'] for t in selected_topics]
    
    def get_selected_topics(self) -> List[Dict[str, str]]:
        """
        Get all selected topics from the CSV file.
        
        Returns:
            List of dictionaries containing selection information
        """
        if not os.path.exists(self.csv_file):
            return []
        
        selections = []
        with open(self.csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                selections.append(row)
        
        return selections
    
    def get_student_selection(self, student_id: str) -> Optional[Dict[str, str]]:
        """
        Get a specific student's topic selection.
        
        Args:
            student_id: Student's unique identifier
            
        Returns:
            Dictionary with selection info or None if no selection
        """
        selections = self.get_selected_topics()
        for selection in selections:
            if selection['student_id'] == student_id:
                return selection
        return None
    
    def get_unavailable_topic_ids(self) -> List[str]:
        """
        Get list of all topic IDs that are no longer available.
        
        Returns:
            List of topic IDs that have been selected
        """
        selections = self.get_selected_topics()
        return [s['topic_id'] for s in selections]
    
    def display_all_selections(self) -> str:
        """
        Generate a formatted string showing all topic selections.
        
        Returns:
            Formatted string with all selections
        """
        selections = self.get_selected_topics()
        
        if not selections:
            return "No topics have been selected yet."
        
        output = "\n" + "="*70 + "\n"
        output += "SELECTED TOPICS REGISTRY\n"
        output += "="*70 + "\n\n"
        
        for i, sel in enumerate(selections, 1):
            output += f"{i}. Student: {sel['student_name']} (ID: {sel['student_id']})\n"
            output += f"   Topic: {sel['topic_title']} (ID: {sel['topic_id']})\n"
            output += f"   Score: {sel['score']}\n"
            output += f"   Selected: {sel['selected_date']}\n\n"
        
        return output
    
    def clear_all_selections(self) -> None:
        """
        Clear all topic selections from the CSV file.
        Useful for resetting the system for testing.
        """
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
        print(f"✓ All topic selections cleared from {self.csv_file}")

