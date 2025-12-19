# FYP Recommender System - Frontend Integration Guide

## 🎯 Quick Start

### Prerequisites
- Python 3.8+ installed
- Node.js 18+ installed
- Both folders in your workspace

### Step 1: Start the Backend API Server

```bash
cd c:\Users\LENOVO\OneDrive\Desktop\RS_Project_try1
python api_server.py
```

You should see:
```
============================================================
FYP Recommender System - API Server
============================================================
Frontend URL: http://localhost:8080
Backend API: http://localhost:5000/api
ML Fallback: Enabled
============================================================

Starting server...

 * Running on http://0.0.0.0:5000
```

**Keep this terminal open!**

### Step 2: Start the Frontend Dev Server

Open a **new terminal** and run:

```bash
cd c:\Users\LENOVO\OneDrive\Desktop\fyp-navigator-main
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:8080/
  ➜  Network: use --host to expose
```

### Step 3: Open the Application

Open your browser and navigate to: **http://localhost:8080**

## 🎨 Application Features

### Dashboard
- View system statistics
- Quick access to all features
- System status indicators

### Students Management
- **Add Student**: Multi-step form to create student profiles
  - Basic Info (ID, Name, CGPA, Major, Year)
  - Skills (with proficiency levels)
  - Interests (with interest levels)
  - Completed Courses
  - Preferences (hours, team size, domains)
- **View Students**: List all students with search/filter
- **Edit/Delete**: Manage existing student profiles

### Recommendations
1. Select a student from the dropdown
2. Choose number of recommendations (1-10)
3. Click "Generate Recommendations"
4. View results with:
   - Match scores
   - Required skills and courses
   - Detailed explanations
   - Domain categories
5. Save to history for future reference

### History
- View all past recommendation sessions
- Filter by student
- See timestamps and details
- Clear history if needed

## 🔧 API Endpoints

All endpoints are available at `http://localhost:5000/api`

### Students
- `GET /api/students` - List all students
- `GET /api/students/:id` - Get student details
- `POST /api/students` - Create new student
- `PUT /api/students/:id` - Update student
- `DELETE /api/students/:id` - Delete student

### Recommendations
- `POST /api/recommendations` - Generate recommendations
  ```json
  {
    "student_id": "STU001",
    "count": 5
  }
  ```

### History
- `GET /api/history` - Get all history (optional `?student_id=` filter)
- `POST /api/history` - Save recommendations
- `DELETE /api/history` - Clear all history

### Metadata
- `GET /api/options` - Get dropdown options (skills, courses, domains, etc.)
- `GET /api/stats` - Get dashboard statistics

### Health Check
- `GET /api/health` - Check API status

## 🧪 Testing the Integration

### Test Flow 1: Create Student and Get Recommendations

1. **Navigate to "Add Student"**
   - Fill in Student ID: `TEST001`
   - Name: `Ahmad Khan`
   - Major: `Computer Science`
   - Year: `4`
   - CGPA: `3.5`

2. **Add Skills** (Step 2)
   - Python - ADVANCED
   - Machine Learning - INTERMEDIATE
   - TensorFlow - INTERMEDIATE

3. **Add Interests** (Step 3)
   - Artificial Intelligence - VERY_HIGH
   - Data Science - HIGH

4. **Select Courses** (Step 4)
   - Artificial Intelligence
   - Data Structures
   - Statistics

5. **Set Preferences** (Step 5)
   - Max Weekly Hours: 20
   - Team Size: 2
   - Preferred Domains: AI, Data Science

6. **Save Student**

7. **Navigate to "Recommendations"**
   - Select "Ahmad Khan (TEST001)"
   - Set count to 5
   - Click "Generate Recommendations"
   - Review the recommendations with match scores
   - Click "Save to History"

8. **Navigate to "History"**
   - Verify your saved recommendations appear

### Test Flow 2: API Direct Testing

Use curl or browser to test endpoints:

```bash
# Get stats
curl http://localhost:5000/api/stats

# Get options
curl http://localhost:5000/api/options

# Get all students
curl http://localhost:5000/api/students

# Health check
curl http://localhost:5000/api/health
```

## 🐛 Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError: No module named 'flask'"**
```bash
pip install Flask Flask-CORS
```

**Error: "Address already in use"**
- Another process is using port 5000
- Kill the process or change the port in `api_server.py`

**Error: "ML fallback disabled"**
- This is normal if ML model isn't trained yet
- System will work with knowledge-based recommendations only
- To enable: Run `python train_ml_model.py`

### Frontend Issues

**Error: "Failed to fetch"**
- Make sure backend API server is running
- Check that it's running on port 5000
- Verify CORS is enabled (should be automatic)

**Error: "npm: command not found"**
- Install Node.js from https://nodejs.org/

**Port 8080 already in use**
- Change port in `vite.config.ts` (line 10)

### CORS Issues

If you see CORS errors in browser console:
1. Verify Flask-CORS is installed: `pip list | grep Flask-CORS`
2. Check that `api_server.py` has `CORS(app)` line
3. Restart the backend server

## 📊 Data Storage

All data is stored in JSON files in the `data/` directory:

- `data/students.json` - Student profiles
- `data/recommendations_history.json` - Recommendation history
- `selected_topics.csv` - Topic selection tracking

## 🔄 Development Workflow

### Making Backend Changes

1. Stop the backend server (Ctrl+C)
2. Edit Python files
3. Restart: `python api_server.py`
4. Frontend will automatically reconnect

### Making Frontend Changes

- Vite has hot module replacement (HMR)
- Changes appear instantly in browser
- No need to restart the dev server

## 🚀 Production Deployment

### Backend
```bash
# Use a production WSGI server like gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

### Frontend
```bash
cd fyp-navigator-main
npm run build
# Deploy the 'dist' folder to your web server
```

## 📝 Notes

- Backend runs on port **5000**
- Frontend runs on port **8080**
- Both must be running simultaneously
- Data persists between restarts
- ML fallback activates when knowledge-based system returns < 3 recommendations

## 🎓 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Browser (Port 8080)                   │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ Dashboard  │  │   Students   │  │ Recommendations│  │
│  └────────────┘  └──────────────┘  └────────────────┘  │
└───────────────────────────┬─────────────────────────────┘
                            │ HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Flask API Server (Port 5000)                │
│  ┌────────────────────────────────────────────────────┐ │
│  │  /api/students  /api/recommendations  /api/history │ │
│  └────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Python Backend Modules                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │FYPRecommender│  │KnowledgeBase │  │StorageManager│  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │MLRecommender │  │TopicTracker  │                    │
│  └──────────────┘  └──────────────┘                    │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  JSON Files   │
                    │  (data/*.json)│
                    └───────────────┘
```

## 🆘 Support

If you encounter issues:
1. Check both terminal windows for error messages
2. Verify both servers are running
3. Check browser console for errors (F12)
4. Ensure all dependencies are installed
5. Try restarting both servers

Happy coding! 🎉
