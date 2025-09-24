@echo off
python "D:\Unreal Projects\AvatarCPP7\Scripts\run_headless_a2f.py"
if %errorlevel% neq 0 (
    echo Script failed with error code %errorlevel%
    pause
    exit /b %errorlevel%
)
echo run_headless_a2f Script completed successfully


python "D:\Unreal Projects\AvatarCPP7\Scripts\set_a2f.py"
if %errorlevel% neq 0 (
    echo Script failed with error code %errorlevel%
    pause
    exit /b %errorlevel%
)
echo set_a2f Script completed successfully
pause