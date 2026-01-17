@echo off
echo BPM Tool - GitHub Push Script
echo ================================
echo.

echo Step 1: Configuring Git user...
git config --global user.name "Mayuk"
git config --global user.email "mayuk.sj@gmail.com"

echo.
echo Step 2: Initializing repository...
git init

echo.
echo Step 3: Adding all files...
git add .

echo.
echo Step 4: Creating initial commit...
git commit -m "Initial commit: BPM Workflow Designer with Gradio"

echo.
echo Step 5: Setting up remote repository...
echo Please create a new repository on GitHub first:
echo 1. Go to https://github.com/mayuksjgit
echo 2. Click 'New repository'
echo 3. Name it: bpm-workflow-designer
echo 4. Make it public
echo 5. Don't initialize with README
echo 6. Click 'Create repository'
echo.
pause

echo.
echo Step 6: Adding remote origin...
git remote add origin https://github.com/mayuksjgit/bpm-workflow-designer.git

echo.
echo Step 7: Setting main branch...
git branch -M main

echo.
echo Step 8: Pushing to GitHub...
echo You will be prompted for your GitHub credentials
echo Use your email: mayuk.sj@gmail.com
echo For password, use a Personal Access Token (not your account password)
echo.
git push -u origin main

echo.
echo Done! Check your repository at:
echo https://github.com/mayuksjgit/bpm-workflow-designer
echo.
pause