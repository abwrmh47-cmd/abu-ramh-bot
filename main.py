import phonenumbers
from phonenumbers import carrier, geocoder, PhoneNumberType
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform

KV = """
#:import dp kivy.metrics.dp
BoxLayout:
    orientation: "vertical"
    padding: dp(18)
    spacing: dp(12)
    canvas.before:
        Color:
            rgba: (0.035, 0.055, 0.095, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: "أبو رمح"
        font_size: "30sp"
        bold: True
        color: (0.2, 0.72, 1, 1)
        size_hint_y: None
        height: dp(54)
    Label:
        text: "فاحص معلومات أرقام الهاتف العامة"
        color: (0.8, 0.86, 0.94, 1)
        size_hint_y: None
        height: dp(28)
    TextInput:
        id: phone
        hint_text: "أدخل الرقم بصيغته الدولية، مثال +9647XXXXXXXXX"
        multiline: False
        input_type: "tel"
        size_hint_y: None
        height: dp(54)
        font_size: "16sp"
    BoxLayout:
        size_hint_y: None
        height: dp(50)
        spacing: dp(8)
        Button:
            text: "فحص الرقم"
            on_release: app.check_number()
        Button:
            text: "مسح"
            size_hint_x: .35
            on_release: app.clear()
    Label:
        text: "النتيجة"
        color: (0.2, 0.72, 1, 1)
        size_hint_y: None
        height: dp(28)
    ScrollView:
        Label:
            id: result
            text: "ستظهر هنا معلومات الترقيم المتاحة."
            color: (0.92, 0.94, 0.98, 1)
            halign: "right"
            valign: "top"
            text_size: self.width - dp(20), None
            size_hint_y: None
            height: max(self.texture_size[1] + dp(24), dp(100))
    Label:
        text: "لا يكشف التطبيق هوية مالك الرقم أو بياناته الخاصة."
        color: (0.62, 0.69, 0.79, 1)
        font_size: "11sp"
        size_hint_y: None
        height: dp(34)
"""
class AbuRamhApp(App):
    def build(self):
        self.title = "أبو رمح"
        if platform != "android":
            Window.size = (400, 740)
        return Builder.load_string(KV)
    def clear(self):
        self.root.ids.phone.text = ""
        self.root.ids.result.text = "ستظهر هنا معلومات الترقيم المتاحة."
    def check_number(self):
        raw = self.root.ids.phone.text.strip()
        out = self.root.ids.result
        try:
            n = phonenumbers.parse(raw, None)
        except Exception:
            out.text = "تعذر قراءة الرقم. استخدم الصيغة الدولية مثل +964..."
            return
        if not phonenumbers.is_possible_number(n):
            out.text = "الرقم لا يبدو بطول صحيح. تحقق من كتابته."
            return
        region = geocoder.description_for_number(n, "ar") or "غير متاح"
        operator = carrier.name_for_number(n, "ar") or "غير متاح في قاعدة البيانات"
        t = phonenumbers.number_type(n)
        kind = "محمول" if t == PhoneNumberType.MOBILE else ("أرضي" if t == PhoneNumberType.FIXED_LINE else "غير محدد")
        valid = "نعم" if phonenumbers.is_valid_number(n) else "غير مؤكد"
        fmt = phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        out.text = (f"الرقم الدولي: {fmt}\\nرمز الدولة: +{n.country_code}\\n"
                    f"الدولة/المنطقة: {region}\\nنوع الرقم: {kind}\\n"
                    f"مطابقة خطة الترقيم: {valid}\\nشركة الاتصالات: {operator}\\n\\n"
                    "هذه بيانات ترقيم عامة؛ لا تثبت نشاط الرقم أو هوية مالكه.")
if __name__ == "__main__":
    AbuRamhApp().run()
