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
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
