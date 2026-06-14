[app]
title = Ziko Parents App
package.name = zikoparentsapp
package.domain = org.ziko
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# إضافة مكتبتي openssl و sqlite3 لضمان عمل requests و urllib3 بدون مشاكل توافق
requirements = python3, kivy==2.3.0, kivymd==1.2.0, openssl, sqlite3, requests, urllib3, certifi, idna, charset_normalizer

orientation = portrait
fullscreen = 0

# حصر البناء على معمارية الهواتف الحديثة لمنع تداخل ملفات الربط (.so)
android.archs = arm64-v8a

# قبول الرخص تلقائياً صامتاً
android.accept_sdk_license = True

# الإصدارات الذهبية والمستقرة والمجربة
android.api = 33
android.minapi = 26
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 0
