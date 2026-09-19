@echo off
cd /d "%~dp0"
where python >nul 2>nul
if not errorlevel 1 (
  python preview.py
) else (
  where py >nul 2>nul
  if errorlevel 1 (
    echo Python 3 is required. Please activate your Python environment.
  ) else (
    py -3 preview.py
  )
)
pause
