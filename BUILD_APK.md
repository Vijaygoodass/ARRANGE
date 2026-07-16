# 📱 BUILD ANDROID APK - Complete Guide

## 🎯 Option 1: Build on Your Computer (Recommended)

### ⚙️ Prerequisites (Install These):

1. **Python 3.9+**
   ```bash
   # Download from python.org
   python --version  # Check version
   ```

2. **Java Development Kit (JDK 11 or higher)**
   ```bash
   # Download from oracle.com or use OpenJDK
   java -version  # Check version
   ```

3. **Android SDK**
   - Download Android Studio from developer.android.com
   - Or download Android SDK Command-line tools

4. **Android NDK** (for native libraries)
   - Download from developer.android.com/ndk

### 📦 Step 1: Install Buildozer

```bash
# On Windows, Mac, or Linux
pip install buildozer cython
```

### 🔧 Step 2: Configure Environment Variables

**Windows:**
```bash
# Set these in Environment Variables:
ANDROID_SDK_ROOT = C:\Users\YourName\AppData\Local\Android\Sdk
ANDROID_NDK_ROOT = C:\Users\YourName\Android\ndk\25.1.8937393
JAVA_HOME = C:\Program Files\Java\jdk-11
```

**Mac/Linux:**
```bash
export ANDROID_SDK_ROOT=~/Android/Sdk
export ANDROID_NDK_ROOT=~/Android/ndk/25.1.8937393
export JAVA_HOME=/usr/libexec/java_home
```

### 🏗️ Step 3: Build the APK

**Navigate to your project directory:**
```bash
cd ARRANGE
```

**Build the APK:**
```bash
buildozer android debug
```

**For release version (to publish):**
```bash
buildozer android release
```

### ⏱️ Build Time:
- First build: **30-60 minutes** (downloads all dependencies)
- Subsequent builds: **5-10 minutes**

### 📍 Where's the APK?

After successful build:
```
ARRANGE/bin/arrange-1.0-debug.apk
```

Or for release:
```
ARRANGE/bin/arrange-1.0-release.apk
```

---

## 🎯 Option 2: Use Pre-built APK (Easiest - Coming Soon)

Download ready-made APK from GitHub Releases (no building needed!)

---

## 📱 Installation on Android Phone

### Method 1: Direct Install (Easiest)

1. **Transfer APK to your phone**
   - Connect phone via USB
   - Copy `arrange-1.0-debug.apk` to phone storage
   - OR email it to yourself and download

2. **Install the APK**
   - Open file manager on phone
   - Navigate to the APK file
   - Tap to install
   - May need to enable "Unknown Sources" in Settings > Security

### Method 2: ADB (Command Line)

```bash
# Connect phone via USB
# Enable USB Debugging on phone (Settings > Developer Options)

adb install arrange-1.0-debug.apk
```

### ✅ Done!
The app will appear on your home screen as "ARRANGE File Organizer"

---

## 🚀 Using the App on Android

### First Launch:
1. Open "ARRANGE" app
2. Tap "➕ Add" button
3. Enter folder path (e.g., `/storage/emulated/0/Download`)
4. Tap "✓ Add"

### Common Android Paths:
- **Downloads**: `/storage/emulated/0/Download` or `/sdcard/Download`
- **Pictures**: `/storage/emulated/0/Pictures`
- **Documents**: `/storage/emulated/0/Documents`
- **Music**: `/storage/emulated/0/Music`
- **Videos**: `/storage/emulated/0/Movies`

### Organize Files:
1. Select directory from dropdown
2. Tap "⚡ Organize Now"
3. Watch the log as files get organized
4. Done! ✅

---

## 🔧 Troubleshooting

### Problem: "Permission Denied" when organizing
**Solution:**
- Go to Settings > Apps > ARRANGE > Permissions
- Enable "Files and Media" or "Storage" permission

### Problem: Can't find folder path
**Solution:**
- On newer Android (11+), use internal storage paths
- Try: `/storage/emulated/0/` instead of `/sdcard/`

### Problem: Build fails
**Solution:**
```bash
# Clear cache and rebuild
buildozer android clean
buildozer android debug
```

### Problem: Kivy not found
**Solution:**
```bash
pip install kivy==2.2.1
pip install kivy_garden
```

---

## 📊 APK Details

- **App Name**: ARRANGE
- **Package Name**: org.fileorganizer.arrange
- **Min Android Version**: Android 5.0+ (API 21)
- **Target Android Version**: Android 12+ (API 31)
- **File Support**: 200+ file types
- **APK Size**: ~50-100 MB (varies)

---

## 🎓 Advanced: Customize the Build

Edit `buildozer.spec` to change:
- App name
- Icon (add your icon)
- Permissions
- Android version
- Package name

Then rebuild:
```bash
buildozer android debug
```

---

## 📚 Helpful Links

- Buildozer Docs: https://buildozer.readthedocs.io/
- Kivy Docs: https://kivy.org/doc/stable/
- Android Permissions: https://developer.android.com/guide/topics/permissions/overview
- ADB Setup: https://developer.android.com/studio/command-line/adb

---

## ❓ Need Help?

Check the logs:
```bash
buildozer android debug -- --verbose
```

Or check `buildozer.log` file after build attempt.
