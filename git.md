# Create a Markdown (.md) file for the Git Command Guide
import pypandoc

content = """
# Git Command Guide for Your Project (DocumentPortal)

This guide contains the essential Git commands you need for managing your ML/LLM projects professionally.

---

# 1️⃣ Initial Setup (One-Time Only)

## Configure Git Username and Email
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

Explanation:
Sets your global identity for commits. Required before pushing to GitHub.

---

# 2️⃣ Initialize Repository

## Initialize Git
git init

Explanation:
Creates a new Git repository in your project folder.

## Check Repository Status
git status

Explanation:
Shows modified, staged, and untracked files.

---

# 3️⃣ Staging and Committing Changes

## Stage All Files
git add .

## Stage Specific File
git add filename.py

## Commit Changes
git commit -m "feat: initial dockerized LLM app"

Explanation:
Creates a snapshot of staged changes with a meaningful message.

---

# 4️⃣ Branching Strategy

## Rename Default Branch to main
git branch -M main

## Create and Switch to New Branch
git checkout -b develop

## Create Feature Branch
git checkout -b feature/add-validation

Explanation:
Use branches to isolate development work.

Recommended Structure:
- main → production-ready code
- develop → active development
- feature/* → new features
- fix/* → bug fixes

---

# 5️⃣ Merging Branches

## Merge Feature into Develop
git checkout develop
git merge feature/add-validation

## Delete Merged Branch
git branch -d feature/add-validation

---

# 6️⃣ Undo & Fix Mistakes

## Unstage File
git restore --staged filename.py

## Discard Changes in File
git restore filename.py

## Undo Last Commit (Keep Changes)
git reset --soft HEAD~1

## Undo Last Commit (Delete Changes)
git reset --hard HEAD~1

## Amend Last Commit Message
git commit --amend

---

# 7️⃣ Working with Remote (GitHub)

## Add Remote Repository
git remote add origin https://github.com/username/repo.git

## Check Remote
git remote -v

## Push Code to GitHub
git push -u origin main

## Push Current Branch
git push

---

# 8️⃣ View History and Differences

## View Commit History
git log --oneline --graph

## See File Differences
git diff

## Compare Between Commits
git diff <commit_id>

---

# 9️⃣ Git Tags (Versioning)

## Create Tag
git tag -a v1.0.0 -m "Initial stable release"

## Push Tag
git push origin v1.0.0

---

# 🔟 Stash Changes (Temporary Save)

## Save Current Work
git stash

## View Stashes
git stash list

## Apply Stash
git stash apply

---

# 🏆 Professional Commit Message Examples

feat(streamlit): added document upload UI
fix(docker): resolved editable install issue
chore(gitignore): removed logs and env
refactor(config): improved path handling

---

# ✅ Minimum Commands You Must Master

- git status
- git add
- git commit
- git branch
- git checkout
- git merge
- git push
- git pull
- git reset
- git log

---

# 🚀 Recommended Workflow for Your ML/LLM Projects

1. Work on feature branch
2. Commit clean, meaningful messages
3. Merge into develop
4. Test thoroughly
5. Merge into main
6. Tag stable version
7. Deploy
"""

output_path = "/mnt/data/Git_Command_Guide_DocumentPortal.md"

pypandoc.convert_text(content, 'md', format='md', outputfile=output_path, extra_args=['--standalone'])

output_path
