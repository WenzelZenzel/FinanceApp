[app]

# Название приложения
title = FinanceApp

# Пакет приложения (как Java package)
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
android.arch = arm64-v8a
android.build_tools_version = 33.0.2  # стабильная версия Build-Tools

# Права
android.permissions = INTERNET

# Логирование
log_level = 2

# Включаем файлы с расширениями py, kv, db, png, jpg
source.include_exts = py,png,jpg,kv,db

