# FYP Navigator

**FYP Navigator** is a comprehensive Recommender System designed to assist students in selecting the most suitable Final Year Project (FYP) topics. It utilizes a hybrid approach, combining **Knowledge-Based Filtering** with **Machine Learning** techniques to provide personalized and accurate recommendations.

## 🚀 Features

- **Personalized Recommendations:** Tailors topic suggestions based on student skills, interests, and academic background.
- **Hybrid Engine:** Merges rule-based logic with ML predictions to handle complex constraints and "cold start" scenarios.
- **Feasibility Analysis:** Evaluates project feasibility based on available resources and technical requirements.
- **Risk Assessment:** detailed risk scores for proposed topics to help students make informed decisions.
- **Modern UI:** A sleek, responsive web interface built with React and Tailwind CSS.

## 🛠️ Tech Stack

### Frontend
- **Framework:** React (Vite)
- **Styling:** Tailwind CSS
- **Language:** JavaScript/TypeScript

### Backend
- **Server:** Python (Flask)
- **Logic:** Custom Inference Engine + ML Models
- **Data:** CSV/JSON based knowledge base

## 📦 Installation & Setup

### Prerequisites
- Node.js & npm
- Python 3.8+

### 1. Clone the Repository
```bash
git clone https://github.com/abdul-rehman-0609/FYP_Navigator.git
cd FYP_Navigator
```

### 2. Backend Setup
Navigate to the backend directory and start the API server:
```bash
cd Backend
# Install dependencies (if requirements.txt exists)
# pip install -r requirements.txt
python api_server.py
```

### 3. Frontend Setup
Open a new terminal, navigate to the frontend directory, and start the development server:
```bash
cd Frontend
npm install
npm run dev
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.