@echo off

git pull
git diff --no-prefix -U200
git add .
git commit
git push
pause
