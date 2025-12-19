const API_BASE = 'http://localhost:5000/api';

export interface Skill {
  name: string;
  proficiency: 'NOVICE' | 'INTERMEDIATE' | 'ADVANCED' | 'EXPERT';
}

export interface Interest {
  domain: string;
  level: 'LOW' | 'MEDIUM' | 'HIGH' | 'VERY_HIGH';
}

export interface Preferences {
  max_weekly_hours: number;
  team_size: number;
  preferred_domains: string[];
}

export interface Student {
  id: string;
  name: string;
  cgpa: number;
  major: string;
  year: number;
  skills: Skill[];
  interests: Interest[];
  completed_courses: string[];
  preferences: Preferences;
}

export interface Recommendation {
  topic_id: string;
  title: string;
  description: string;
  match_score: number;
  required_skills: string[];
  required_courses: string[];
  explanation: string;
  domain: string;
  feasibility_score: number;
  risk_level: string;
  match_reasons: string[];
  risk_reasons: string[];
}

export interface HistoryEntry {
  id: string;
  student_id: string;
  student_name: string;
  timestamp: string;
  recommendations: Recommendation[];
}

export interface DropdownOptions {
  skills: string[];
  courses: string[];
  domains: string[];
  majors: string[];
  proficiency_levels: string[];
  interest_levels: string[];
}

// API Functions
export const api = {
  // Students
  async getStudents(): Promise<Student[]> {
    try {
      const res = await fetch(`${API_BASE}/students`);
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || `Server error: ${res.status}`);
      }
      return await res.json();
    } catch (error) {
      console.error("Error fetching students:", error);
      throw error;
    }
  },

  async getStudent(id: string): Promise<Student> {
    try {
      const res = await fetch(`${API_BASE}/students/${id}`);
      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }
      return await res.json();
    } catch (error) {
      console.error("Error fetching student:", error);
      throw error;
    }
  },

  async createStudent(student: Omit<Student, 'id'>): Promise<Student> {
    try {
      const res = await fetch(`${API_BASE}/students`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...student, id: crypto.randomUUID() }),
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || `Server error: ${res.status}`);
      }
      return await res.json();
    } catch (error) {
      console.error("Error creating student:", error);
      throw error;
    }
  },

  async updateStudent(id: string, student: Partial<Student>): Promise<Student> {
    try {
      const res = await fetch(`${API_BASE}/students/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(student),
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || `Server error: ${res.status}`);
      }
      return await res.json();
    } catch (error) {
      console.error("Error updating student:", error);
      throw error;
    }
  },

  async deleteStudent(id: string): Promise<void> {
    try {
      const res = await fetch(`${API_BASE}/students/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
    } catch (error) {
      console.error("Error deleting student:", error);
      throw error;
    }
  },

  // Recommendations
  async getRecommendations(studentId: string, count: number = 5): Promise<Recommendation[]> {
    try {
      const res = await fetch(`${API_BASE}/recommendations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: studentId, count }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || `Server error: ${res.status}`);
      }

      return await res.json();
    } catch (error) {
      console.error("Recommendation Fetch Error:", error);
      throw error;
    }
  },

  async selectTopic(studentId: string, topicId: string, score: number): Promise<void> {
    try {
      const res = await fetch(`${API_BASE}/select_topic`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: studentId, topic_id: topicId, score }),
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || `Server error: ${res.status}`);
      }
    } catch (error) {
      console.error("Error selecting topic:", error);
      throw error;
    }
  },

  // History
  async getHistory(studentId?: string): Promise<HistoryEntry[]> {
    try {
      const url = studentId
        ? `${API_BASE}/history?student_id=${studentId}`
        : `${API_BASE}/history`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      return await res.json();
    } catch (error) {
      console.error("Error fetching history:", error);
      throw error;
    }
  },

  async saveToHistory(studentId: string, recommendations: Recommendation[]): Promise<void> {
    try {
      const res = await fetch(`${API_BASE}/history`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: studentId, recommendations }),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
    } catch (error) {
      console.error("Error saving history:", error);
      throw error;
    }
  },

  async clearHistory(): Promise<void> {
    try {
      const res = await fetch(`${API_BASE}/history`, { method: 'DELETE' });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
    } catch (error) {
      console.error("Error clearing history:", error);
      throw error;
    }
  },

  // Options
  async getOptions(): Promise<DropdownOptions> {
    try {
      const res = await fetch(`${API_BASE}/options`);
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || `Server error: ${res.status}`);
      }
      return await res.json();
    } catch (error) {
      console.error("Error fetching options:", error);
      throw error;
    }
  },

  // Stats
  async getStats(): Promise<{ students: number; recommendations: number; topics: number }> {
    try {
      const res = await fetch(`${API_BASE}/stats`);
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      return await res.json();
    } catch (error) {
      console.error("Error fetching stats:", error);
      throw error;
    }
  },
};
