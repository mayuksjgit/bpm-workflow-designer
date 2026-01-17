@echo off
echo 🛑 Stopping BPM Workflow Designer...
echo.

echo Stopping and removing containers...
docker-compose down

echo.
echo Checking if containers are stopped...
docker ps -a | findstr bpm-workflow-designer

echo.
echo ✅ BPM Workflow Designer stopped successfully!
echo.
pause