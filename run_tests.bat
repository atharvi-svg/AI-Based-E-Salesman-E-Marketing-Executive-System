@echo off
echo Running Backend Unit Tests...
python backend/test_backend.py
if %ERRORLEVEL% NEQ 0 (
    echo Backend tests failed!
    pause
    exit /b %ERRORLEVEL%
)

echo Running End-to-End Workflow Tests...
python test_e2e_workflow.py
if %ERRORLEVEL% NEQ 0 (
    echo E2E tests failed!
    pause
    exit /b %ERRORLEVEL%
)

echo All tests passed successfully!
pause
