@echo off
echo 🐳 Building BPM Workflow Designer Docker Image...
echo.

echo Step 1: Building Docker image...
docker build -t bpm-workflow-designer .

echo.
echo Step 2: Checking if image was built successfully...
docker images bpm-workflow-designer

echo.
echo ✅ Docker image built successfully!
echo.
echo To run the container:
echo   docker-compose up -d
echo.
echo Or run directly:
echo   docker run -d -p 80:80 --name bpm-tool bpm-workflow-designer
echo.
pause