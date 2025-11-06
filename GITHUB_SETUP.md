# How to Push to GitHub

Follow these steps to push your HR Video Analyzer project to GitHub:

## Step 1: Initialize Git Repository (if not already done)

```bash
cd /Users/thejasvk/Downloads/Stevens-Sem-3/AgileAnalysts
git init
```

## Step 2: Check Current Status

```bash
git status
```

This will show you which files are tracked, untracked, or modified.

## Step 3: Add Files to Git

Add all files you want to commit:

```bash
# Add all files
git add .

# Or add specific files/directories
git add hr-video-analyzer/
git add README.md
```

**Note:** The `.gitignore` file will automatically exclude:
- `node_modules/` (React dependencies)
- `venv/` (Python virtual environment)
- `uploads/` (uploaded videos and results)
- `__pycache__/` (Python cache files)
- `build/` (React build files)

## Step 4: Commit Your Changes

```bash
git commit -m "Initial commit: HR Video Analyzer with React frontend and FastAPI backend"
```

Or use a more descriptive message:

```bash
git commit -m "Add React frontend for HR Video Analyzer

- Created React frontend with video upload and results display
- Integrated with FastAPI backend
- Added CORS support
- Configured for both development and production modes"
```

## Step 5: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name**: `hr-video-analyzer` (or your preferred name)
   - **Description**: "HR Video Analyzer - Full-stack application with React frontend and FastAPI backend for video analysis and face detection"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (since you already have these)
5. Click **"Create repository"**

## Step 6: Add GitHub Remote

After creating the repository, GitHub will show you commands. Use the HTTPS or SSH URL:

**Using HTTPS:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/hr-video-analyzer.git
```

**Using SSH (if you have SSH keys set up):**
```bash
git remote add origin git@github.com:YOUR_USERNAME/hr-video-analyzer.git
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 7: Verify Remote

```bash
git remote -v
```

This should show your remote repository URL.

## Step 8: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

If you're using a different branch name or if GitHub uses `master`:
```bash
git push -u origin master
```

## Step 9: Verify on GitHub

Go to your repository on GitHub and verify that all files are uploaded correctly.

## Troubleshooting

### If you get authentication errors:

**For HTTPS:**
- You may need to use a Personal Access Token instead of password
- Go to GitHub Settings > Developer settings > Personal access tokens
- Generate a new token with `repo` permissions
- Use the token as your password when pushing

**For SSH:**
- Make sure you have SSH keys set up with GitHub
- Follow GitHub's guide: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### If you need to update later:

```bash
# Make your changes, then:
git add .
git commit -m "Your commit message"
git push
```

### If you want to exclude the video file:

The video file `shriteja-video.mov` is currently untracked. If you want to exclude it, add this to `.gitignore`:

```bash
# Add to .gitignore
*.mov
*.mp4
```

## Quick Reference Commands

```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Push
git push

# Pull latest changes
git pull

# View remote
git remote -v

# View commit history
git log
```

