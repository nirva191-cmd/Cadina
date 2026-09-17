[app]

# (str) Title of your application
title = Main Message App

# (str) Package name
package.name = mainmessageapp

# (str) Package domain (needed for android packaging)
package.domain = org.example

# (str) Source files where the let and python code is located
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to include (let empty to include all files)
source.include_dir = 

# (list) List of inclusion/exclusion patterns for source files
source.exclude_exts = spec

# (list) List of exclusions using pattern matching
source.exclude_dirs = tests, bin, venv, .venv

# (str) Application versioning
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,jnius

# (list) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,SEND_SMS,RECEIVE_SMS,READ_SMS,CALL_PHONE,READ_PHONE_STATE,READ_CALL_LOG,PROCESS_OUTGOING_CALLS

# (str) Supported architectures
android.archs = arm64-v8a, armeabi-v7a

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
