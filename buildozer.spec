[app]
title = Ziko Parents App
package.name = zikoparentsapp
package.domain = org.ziko
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, urllib3, certifi, idna, charset_normalizer
orientation = portrait
fullscreen = 0

# تعديل المعماريات لدعم الهواتف الحديثة والقديمة لضمان استقرار التجميع
android.archs = arm64-v8a, armeabi-v7a

# قبول الرخص تلقائياً صامتاً
android.accept_sdk_license = True

# تحديد الإصدارات الذهبية والمستقرة للـ SDK والـ NDK المتوافقة 100% مع Kivy
android.api = 33
android.minapi = 26
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 0
