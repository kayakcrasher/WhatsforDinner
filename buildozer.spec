[app]

# (str) Title of your application
title = What's for Dinner

# (str) Package name
package.name = whatsfordinner

# (str) Package domain (needed for android/ios packaging)
package.domain = com.yourname

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all)
source.include_exts = py,png,jpg,kv,atlas,json,db

# (list) Application version
version = 0.1.0

# (list) Application requirements
# SJBillingClient requires pyjnius and the billing gradle dependency
requirements = python3,kivy,sjbillingclient,pyjnius,android

# (str) Custom source folders for requirements
# source.include_exts already covers our src/ and assets/ folders

# (list) Permissions
android.permissions = INTERNET, com.android.vending.BILLING

# (str) Android API to use (Android 13+ for Play Store compliance)
android.api = 33

# (int) Minimum API your app will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Enable Android App Bundle (AAB) for Play Store
android.appbundle = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android application meta-data to set (key=value pairs)
android.meta_data =

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) The Android gradle dependencies
android.gradle_dependencies = com.android.billingclient:billing:7.1.1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (str) Path to build artifact storage
build_dir = ./.buildozer

# (str) Path to store the app data
bin_dir = ./bin
