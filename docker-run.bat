@echo off
echo 🐳 Starting BPM Workflow Designer with Docker Compose...
echo.

echo Stopping any existing containers...
docker-compose down

echo.
echo Starting containers in detached mode...
docker-compose up -d

echo.
echo Waiting for container to be ready...
timeout /t 10 /nobreak > nul

echo.
echo Checking container status...
docker-compose ps

echo.
echo 🎉 BPM Workflow Designer is now running!
echo.
echo 🌐 Access your application at:
echo   http://localhost
echo   http://localhost:80
echo.
echo 📊 To view logs:
echo   docker-compose logs -f
echo.
echo 🛑 To stop:
echo   docker-compose down
echo.
pause