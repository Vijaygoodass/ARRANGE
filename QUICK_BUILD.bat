@echo off
REM Quick build script for Windows

echo ========================================
echo ARRANGE Android APK Builder (Windows)
echo ========================================
echo.

REM Check if buildozer is installed
python -m pip show buildozer >nul 2>&1
if errorlevel 1 (
    echo Buildozer not found. Installing...
    pip install buildozer cython kivy
)

REM Check Python version
echo.
echo Checking Python version...
python --version
echo.

echo 🔨 Starting APK build...
echo.

REM Clean previous builds
echo 🧹 Cleaning previous build files...
buildozer android clean

echo.
echo 🏗️ Building APK (this may take 10-30 minutes)...
echo.

REM Build APK
buildozer android debug

echo.
echo ========================================
echo Build Status Check
echo ========================================

if exist "bin\arrange-1.0-debug.apk" (
    echo ✅ APK built successfully!
    echo 📍 Location: bin\arrange-1.0-debug.apk
    echo.
    echo 📱 Next steps:
    echo 1. Transfer APK to your Android phone
    echo 2. Install by tapping the APK file
    echo 3. Grant required permissions
    echo 4. Start organizing files!
) else (
    echo ❌ Build failed. Check logs above.
    echo 📋 Logs: buildozer.log
)

echo.
echo ========================================
pause
