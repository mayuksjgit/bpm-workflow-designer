# GitHub Setup Guide for BPM Tool

## Step 1: Configure Git (One-time setup)
```bash
git config --global user.name "Your Name"
git config --global user.email "mayuk.sj@gmail.com"
```

## Step 2: Initialize Repository
```bash
git init
git add .
git commit -m "Initial commit: BPM Workflow Designer"
```

## Step 3: Create GitHub Repository
1. Go to https://github.com/mayuksjgit
2. Click "New repository" (green button)
3. Repository name: `bpm-workflow-designer`
4. Description: `Visual BPM tool built with Python and Gradio`
5. Make it Public
6. Don't initialize with README (we already have one)
7. Click "Create repository"

## Step 4: Connect Local to GitHub
```bash
git remote add origin https://github.com/mayuksjgit/bpm-workflow-designer.git
git branch -M main
git push -u origin main
```

## Step 5: Authentication Options

### Option A: Personal Access Token (Recommended)
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with repo permissions
3. Use token as password when prompted

### Option B: GitHub CLI (Easiest)
```bash
# Install GitHub CLI first
gh auth login
git push -u origin main
```

## Step 6: Verify Upload
- Check your repository at: https://github.com/mayuksjgit/bmp-workflow-designer
- Verify all files are uploaded
- Check that README.md displays properly

## Security Note
Never store passwords in code or share them publicly. Use tokens or SSH keys for authentication.