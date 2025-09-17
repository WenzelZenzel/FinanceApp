[app]

# Название приложения
title = FinanceApp

# Пакет приложения
package.name = financeapp
package.domain = org.example

# Основной скрипт
source.main = main.py

# Версия приложения
version = 1.0

# Требуемые Python-пакеты
requirements = python3,kivy,matplotlib,numpy,sqlite3

# Android настройки
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a, armeabi-v7a
android.build_tools_version = 33.0.2  # стабильная версия
android.allow_backup = True
# Права
android.permissions = INTERNET
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
# Логирование
log_level = 2
source.dir = .
# Включаем файлы с расширениями py, kv, db, png, jpg
source.include_exts = py,png,jpg,kv,db

orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
#ios.ios_deploy_dir = ../ios_deploy
# Or specify URL and branch
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# (bool) Whether or not to sign the code
ios.codesign.allowed = false
