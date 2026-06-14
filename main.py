import requests
import json
from threading import Thread

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineListItem

# محاكاة أبعاد الجوال على الكمبيوتر
Window.size = (360, 640)

# ضع هنا رابط الـ Realtime Database الخاص بمشروعك في فايربيس (ينتهي بـ .firebaseio.com)
FIREBASE_URL = "https://your-project-id.firebaseio.com"

KV = '''
ScreenManager:
    LoginScreen:
    DashboardScreen:

<LoginScreen>:
    name: 'login'
    MDFloatLayout:
        md_bg_color: 0.97, 0.98, 0.98, 1
        
        MDLabel:
            text: "🎓\\nسحابة ZIKO PRO"
            font_style: "H4"
            halign: "center"
            pos_hint: {"center_y": 0.75}
            theme_text_color: "Custom"
            text_color: 0.17, 0.24, 0.31, 1

        MDLabel:
            text: "بوابة أولياء الأمور للمتابعة اللحظية"
            font_style: "Subtitle1"
            halign: "center"
            pos_hint: {"center_y": 0.62}
            theme_text_color: "Secondary"

        MDTextField:
            id: student_pass
            hint_text: "أدخل رمز دخول الطالب الموحد"
            halign: "center"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5, "center_y": 0.45}
            mode: "rectangle"

        MDRaisedButton:
            text: "تسجيل الدخول الآمن"
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5, "center_y": 0.32}
            md_bg_color: 0.17, 0.24, 0.31, 1
            on_release: root.verify_login()

<DashboardScreen>:
    name: 'dashboard'
    MDBottomNavigation:
        panel_color: 0.17, 0.24, 0.31, 1
        selected_color_background: 0, 0, 0, 0
        text_color_active: 1, 1, 1, 1

        MDBottomNavigationItem:
            name: 'report'
            text: 'الدرجات'
            icon: 'chart-bar'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)
                MDTopAppBar:
                    title: "كشف درجات الطالب"
                    right_action_items: [["logout", lambda x: app.logout()]]
                    elevation: 2
                    md_bg_color: 0.17, 0.24, 0.31, 1
                ScrollView:
                    MDList:
                        id: marks_list

        MDBottomNavigationItem:
            name: 'alerts'
            text: 'الإشعارات'
            icon: 'bell'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                MDTopAppBar:
                    title: "🔔 الإشعارات الإدارية"
                    elevation: 2
                    md_bg_color: 0.17, 0.24, 0.31, 1
                ScrollView:
                    MDList:
                        id: alerts_list

        MDBottomNavigationItem:
            name: 'chat'
            text: 'المحادثة'
            icon: 'chat'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(5)
                MDTopAppBar:
                    title: "💬 مركز الدعم والتواصل"
                    elevation: 2
                    md_bg_color: 0.17, 0.24, 0.31, 1
                ScrollView:
                    MDList:
                        id: chat_list
                BoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(5)
                    MDTextField:
                        id: chat_input
                        hint_text: "اكتب رسالتك هنا..."
                        mode: "line"
                    MDIconButton:
                        icon: "send"
                        md_bg_color: 0.17, 0.24, 0.31, 1
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        on_release: root.send_message()
'''

class LoginScreen(Screen):
    def verify_login(self):
        password = self.ids.student_pass.text.strip()
        if not password:
            return
        
        # جلب بيانات الطالب بناءً على الرمز الموحد (الـ ID أو الباسورد) مباشرة من الفايربيس
        try:
            response = requests.get(f"{FIREBASE_URL}/students/{password}.json")
            student_data = response.json()
            
            if student_data:
                app = MDApp.get_running_app()
                app.current_student_id = password
                app.student_info = student_data
                
                self.manager.current = 'dashboard'
                self.manager.get_screen('dashboard').load_student_data()
            else:
                self.show_error_dialog("رمز الدخول غير صحيح أو غير مسجل!")
        except Exception as e:
            self.show_error_dialog("فشل الاتصال بالسحابة! تحقق من الإنترنت.")

    def show_error_dialog(self, text):
        dialog = MDDialog(title="تنبيه", text=text, size_hint=(0.8, None))
        dialog.open()

class DashboardScreen(Screen):
    def load_student_data(self):
        self.ids.marks_list.clear_widgets()
        self.ids.alerts_list.clear_widgets()
        app = MDApp.get_running_app()
        
        # 1. شحن الدرجات ديناميكياً من الفايربيس
        marks = app.student_info.get('marks', {})
        for subject, score in marks.items():
            self.ids.marks_list.add_widget(
                ThreeLineListItem(
                    text=f"المادة: {subject}",
                    secondary_text=f"الدرجة: {score}",
                    tertiary_text="الحالة: ممتاز" if int(score) >= 90 else "الحالة: ناجح"
                )
            )
            
        # 2. شحن الإشعارات العامة أو الخاصة بالطالب
        alerts = app.student_info.get('alerts', {})
        for alert_id, alert_text in alerts.items():
            self.ids.alerts_list.add_widget(
                ThreeLineListItem(text="📢 تعميم إداري", secondary_text=alert_text, tertiary_text="مهم جداً")
            )
            
        # 3. تشغيل مستمع الشات في الخلفية بدون تعليق التطبيق
        Thread(target=self.stream_chat_messages, daemon=True).start()

    def stream_chat_messages(self):
        app = MDApp.get_running_app()
        # استماع لحظي للرسائل عبر بروتوكول SSE الخاص بالفايربيس
        try:
            url = f"{FIREBASE_URL}/chats/{app.current_student_id}.json"
            response = requests.get(url, stream=True)
            for line in response.iter_lines():
                if line:
                    # تحديث واجهة الشات فوراً عند استقبال أي رسالة جديدة بالثانية
                    self.ids.chat_list.clear_widgets()
                    # (هنا يتم تفكيك نص الرسائل وعرضها، للتبسيط سنعرض الرسائل المرسلة)
                    pass
        except:
            pass

    def send_message(self):
        msg_text = self.ids.chat_input.text.strip()
        if msg_text:
            app = MDApp.get_running_app()
            # دفع الرسالة للفايربيس بلحظتها
            payload = {"sender": "parent", "text": msg_text}
            requests.post(f"{FIREBASE_URL}/chats/{app.current_student_id}.json", json=payload)
            
            self.ids.chat_list.add_widget(
                ThreeLineListItem(text="👪 ولي الأمر", secondary_text=msg_text, tertiary_text="الآن")
            )
            self.ids.chat_input.text = ""

class ParentsMobileApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.current_student_id = None
        self.student_info = {}
        return Builder.load_string(KV)
    
    def logout(self):
        self.root.current = 'login'

if __name__ == '__main__':
    ParentsMobileApp().run()