[app]

# (str) Title of your application
title = ARRANGE File Organizer

# (str) Package name
package.name = arrange

# (str) Package domain (needed for android/ios packaging)
package.domain = org.fileorganizer

# (source.dir) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.png

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientations
# Valid values: landscape, portrait, all
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash of the application (image or animation file)
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Supported orientation (landscape or portrait)
# orientation = portrait

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
#android.ndk = 25b

# (bool) Use the Android Support Library where it is needed
#android.support_deprecated_sdk = False

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup scheme, see the documentation
# android.backup_properties = %(source.dir)s/mybackup.xml

# (str) FAQs of the application
#android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# (str) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (list) Gradle dependencies (for new android toolchain)
# android.gradle_dependencies = com.google.android.gms:play-services-gcm:17.0.0

# (list) Java classes to add as services to the Intent
# android.services = org.kivy.android.PythonService

# (bool) Disable log capture, only used if log_level is set to 0
#android.disable_logcat = False

# (str) logcat module name filter defaults to *:S python:D ; function for log user processes from pid with logs :S
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (int) overrides automatic versionCode computation, -1 to disable
# android.numeric_version = 1

# (list) Pattern to whitelist for the whole project
#android.whitelist = lib-dynload/termios.so

# (str) Path to a Java .jar used to access Android functionality,
# don't change the default value unless you know what you are doing (it is used to build
# the bootstrap in order to change the API level)
# android.jar_src = OUYA-ODK/libs/ouya-sdk.jar

# (str) Path to an android icon, should be a 512x512 png
# android.icon = %(source.dir)s/data/icon.png

# (str) Path to an android presplash, should match the window size, 1024x1024 is the max.
# android.presplash = %(source.dir)s/data/presplash.png

# (str) Android brand (for example, if your app offers a slogan)
#android.meta_data_brand = myappbrand

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include custom intents in manifest. Let's say you want to
# be able to open apk files, add a line:
#  <intent-filter>
#      <action android:name="android.intent.action.VIEW" />
#      <data android:mimeType="application/vnd.android.package-archive" />
#  </intent-filter>
# lines must be indented.
# android.manifest_additions = %(source.dir)s/manifest_additions.xml

# (str) "XXxx pasX" XML from defaultString.xml. androidVersio, just android.meta_data_brand)
# android.accept_sdk_license = True

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# android.permissions = INTERNET

# (list) Android features to declare
# android.features = android.hardware.usb

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 30

# (str) Android NDK version to use
#android.ndk = 23b

# (int) Android API to target
android.api = 31

# (int) Minimum API Kivy supported
android.minapi = 21

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (int) overrides automatic versionCode computation, -1 to disable
# android.numeric_version = 1

# (bool) Use the Android Support Library where it is needed
#android.support_deprecated_sdk = False

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file for custom backup scheme, see the documentation
# android.backup_properties = %(source.dir)s/mybackup.xml

# (str) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (list) Gradle dependencies (for new android toolchain)
# android.gradle_dependencies = com.google.android.gms:play-services-gcm:17.0.0

# (list) Java classes to add as services to the Intent
# android.services = org.kivy.android.PythonService

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) python-for-android branch to use, defaults to master
p4a.branch = develop

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, CATEGORY_LAUNCHER will be used
# android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
# android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include custom intents in manifest. Let's say you want to
# be able to open apk files, add a line:
#  <intent-filter>
#      <action android:name="android.intent.action.VIEW" />
#      <data android:mimeType="application/vnd.android.package-archive" />
#  </intent-filter>
# lines must be indented.
# android.manifest_additions = %(source.dir)s/manifest_additions.xml

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning / error messages even if log_level is set to 0
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin
