@echo off
echo Creating virtual environment for BPM Tool...
python -m venv bmp_env
echo.
echo Activating virtual environment...
call bmp_env\Scripts\activate.bat
echo.
echo Installing required packages...
pip install gradio
echo.
echo Setup complete! 
echo.
echo To run the application:
echo 1. Activate virtual environment: bmp_env\Scripts\activate.bat
echo 2. Run the app: python enhanced_bpm_tool.py
echo.
pause