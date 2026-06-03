#!/bin/bash
# Simple helper script to automate Git commits and pushes

# Default message if none is provided
MESSAGE=${1:-"feat: complete Triageo app with SQLite persistence, Tailwind UI and CI pipeline"}

echo "Staging changes..."
git add .

echo "Committing with message: '$MESSAGE'..."
git commit -m "$MESSAGE"

# Ensure the branch is named main
git branch -M main

echo "Pushing to GitHub..."
git push -u origin main

echo "Done!"
