#!/bin/bash
# Quick build script for Linux/Mac

echo "========================================"
echo "ARRANGE Android APK Builder"
echo "========================================"

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer not found. Installing..."
    pip install buildozer cython kivy
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]\.[0-9]')
echo "✅ Python version: $PYTHON_VERSION"

echo ""
echo "🔨 Starting APK build..."
echo ""

# Clean previous builds
echo "🧹 Cleaning previous build files..."
buildozer android clean

echo ""
echo "🏗️ Building APK (this may take 10-30 minutes)..."
echo ""

# Build APK
buildozer android debug

echo ""
echo "========================================"
echo "Build Status Check"
echo "========================================"

if [ -f "bin/arrange-1.0-debug.apk" ]; then
    echo "✅ APK built successfully!"
    echo "📍 Location: bin/arrange-1.0-debug.apk"
    echo ""
    echo "📱 Next steps:"
    echo "1. Transfer APK to your Android phone"
    echo "2. Install by tapping the APK file"
    echo "3. Grant required permissions"
    echo "4. Start organizing files!"
else
    echo "❌ Build failed. Check logs above."
    echo "📋 Logs: buildozer.log"
fi

echo ""
echo "========================================"
