@echo off
set /p commitMsg="Enter commit message: "
echo.
git add .
git commit -m "%commitMsg%"
git push origin main
pause
