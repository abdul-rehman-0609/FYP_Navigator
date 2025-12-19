# How to Push Your Projects to GitHub

Since you have two distinct folders (Backend and Frontend), the best practice is to create **two separate repositories** on GitHub or use a **monorepo** approach. Below is the guide for creating separate repositories, which is standard for full-stack applications.

## Prerequisites
1.  You must have **Git** installed on your computer.
2.  You must have a **GitHub account**.

---

## Part 1: Push the Backend (`RS_Project_try1`)

1.  **Log in to GitHub** and create a new repository named `fyp-backend` (or similar).
2.  **Do not** initialize it with README, .gitignore, or License (we already have them locally).
3.  Open your terminal (**PowerShell** or **Command Prompt**).
4.  Navigate to your backend folder:
    ```powershell
    cd c:\Users\LENOVO\OneDrive\Desktop\RS_Project_try1
    ```
5.  Initialize Git and commit your files:
    ```powershell
    git init
    git add .
    git commit -m "Initial commit: Recommender System Backend"
    ```
6.  Link to your new GitHub repository (replace `YOUR_USERNAME` with your actual GitHub username):
    ```powershell
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/fyp-backend.git
    git push -u origin main
    ```

---

## Part 2: Push the Frontend (`fyp-navigator-main`)

1.  Create another new repository on GitHub named `fyp-frontend`.
2.  Navigate to your frontend folder:
    ```powershell
    cd c:\Users\LENOVO\OneDrive\Desktop\fyp-navigator-main
    ```
3.  Initialize and push:
    ```powershell
    git init
    git add .
    git commit -m "Initial commit: React Frontend"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/fyp-frontend.git
    git push -u origin main
    ```

---

## Option 2: Single Repository (Monorepo) - **Recommended for Simplicity**

If you prefer to have just **one GitHub link** for your entire project, follow these steps.

1.  **Stop all running servers** (Ctrl+C in your terminals).
2.  **Create a new folder** on your Desktop called `FYP_Project_Full`.
3.  **Move** both your `RS_Project_try1` folder and `fyp-navigator-main` folder **inside** this new `FYP_Project_Full` folder.
    - Structure should look like:
      ```
      FYP_Project_Full/
      ├── RS_Project_try1/      (Backend)
      └── fyp-navigator-main/   (Frontend)
      ```
4.  **Create a Repository** on GitHub named `fyp-full-project`.
5.  Open your terminal, navigate to the **parent** folder `FYP_Project_Full`:
    ```powershell
    cd c:\Users\LENOVO\OneDrive\Desktop\FYP_Project_Full
    ```
6.  Initialize and push:
    ```powershell
    git init
    git add .
    git commit -m "Initial commit: Full Project"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/fyp-full-project.git
    git push -u origin main
    ```

---

## Useful Tips

- **Ignoring Files:** I have already created a `.gitignore` file in your backend folder to prevent pushing unnecessary files like `.venv`, `__pycache__`, or system logs. The frontend folder already had one.
- **Updates:** Whenever you make changes in the future, just run:
    ```powershell
    git add .
    git commit -m "Describe your changes here"
    git push
    ```
