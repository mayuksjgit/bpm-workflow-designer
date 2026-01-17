@echo off
echo Setting up Git repository for BPM Tool...
echo.

echo Initializing Git repository...
git init

echo Adding files to Git...
git add .

echo Creating initial commit...
git commit -m "Initial commit: BPM Workflow Designer with Gradio"

echo.
echo Git repository initialized successfully!
echo.
echo To push to GitHub:
echo 1. Create a new repository on GitHub (https://github.com/mayuksjgit)
echo 2. Copy the repository URL
echo 3. Run: git remote add origin [YOUR_REPO_URL]
echo 4. Run: git branch -M main
echo 5. Run: git push -u origin main
echo.
pause