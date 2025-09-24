@echo off
pythonw "D:\Unreal Projects\AvatarCPP7\Scripts\run_audio.py"
if %errorlevel% neq 0 (
    echo Script failed with error code %errorlevel%
    exit /b %errorlevel%
)
echo run_audio Script completed successfully
pause