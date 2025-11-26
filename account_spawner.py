from flask import Flask, render_template_string, redirect, url_for
import requests
from faker import Faker
import time
import random
import string

app = Flask(__name__)

# =============================================================
# === 🚨 نقطة التفعيل النهائية: يجب تعديل هذه المتغيرات 🚨 ===
# =============================================================

# 1. استبدل هذا بعنوان URL النهائي: https://ladypopular.com/ajax/user.php
TARGET_URL = "https://ladypopular.com/ajax/user.php"

# 2. أسماء الحقول الحقيقية التي تم جمعها:
FIELD_USERNAME = "reg_user"
FIELD_PASSWORD = "reg_pass"
FIELD_EMAIL = "reg_email"
FIELD_TERMS = "reg_terms"
FIELD_PRIVACY = "reg_privacy"
FIELD_MARKETING = "marketing-consent-choice"

# =============================================================

fake = Faker()

# ترميز صفحة الويب التفاعلية (Template)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MOBY - Phantom Recruiter</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #1a1a2e; color: #fff; text-align: center; padding-top: 50px; }
        .container { background: #333; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 0 20px #000; }
        h1 { color: #f90; }
        .log { background: #000; padding: 10px; margin: 15px 0; border-radius: 5px; text-align: left; max-height: 300px; overflow-y: scroll; }
        .success { color: #5cb85c; }
        .failure { color: #d9534f; }
        .btn { background-color: #f90; color: #000; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>MOBY - منشئ الحسابات الوهمية 😈</h1>
        <p>الضغط على الزر سيطلق محاولة إنشاء حساب واحد (Username = Password).</p>
        <a href="{{ url_for('create_account') }}" class="btn">إنشاء حساب جديد</a>
        <div class="log">
            {% for entry in log %}
                <p class="{{ 'success' if 'نجاح' in entry else 'failure' }}">{{ entry }}</p>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# لتبسيط الأمر، سنستخدم قائمة بسيطة لتخزين نتائج السجلات
RECRUITMENT_LOG = []

def generate_user_data_logic():
    """توليد البيانات: اسم المستخدم هو نفسه كلمة المرور"""
    chars = string.ascii_lowercase + string.digits
    base_name = ''.join(random.choice(chars) for _ in range(8))
    
    username = base_name
    password = base_name
    
    email = fake.user_name() + str(random.randint(1, 999)) + "@" + fake.domain_name()
    
    return username, password, email

def register_account(username, password, email):
    """إرسال طلب POST لتسجيل حساب جديد"""
    session = requests.Session()
    
    payload = {
        FIELD_USERNAME: username,
        FIELD_PASSWORD: password,
        FIELD_EMAIL: email,
        FIELD_TERMS: '1',     
        FIELD_PRIVACY: '1',   
        FIELD_MARKETING: '1', 
    }
    
    try:
        response = session.post(TARGET_URL, data=payload, timeout=15)
        
        if response.status_code == 200 and ("success" in response.text.lower() or "ok" in response.text.lower()):
            log_entry = f"✅ نجاح: {username} | الباسوورد: {password}"
            RECRUITMENT_LOG.insert(0, log_entry) # إضافة الأحدث في الأعلى
        else:
            log_entry = f"❌ فشل: {username} | الحالة: {response.status_code}"
            RECRUITMENT_LOG.insert(0, log_entry) 

    except requests.exceptions.RequestException as e:
        log_entry = f"⛔ خطأ في الاتصال: {e}"
        RECRUITMENT_LOG.insert(0, log_entry)

@app.route('/')
def index():
    """عرض صفحة الويب الرئيسية"""
    return render_template_string(HTML_TEMPLATE, log=RECRUITMENT_LOG)

@app.route('/create', methods=['GET'])
def create_account():
    """نقطة النهاية لتنفيذ عملية إنشاء الحساب"""
    username, password, email = generate_user_data_logic()
    register_account(username, password, email)
    return redirect(url_for('index')) # العودة للصفحة الرئيسية لتحديث السجل

if __name__ == '__main__':
    # يجب أن يستخدم هذا المتغير في Render لفتح البورت
    app.run(host='0.0.0.0', port=random.randint(5000, 8000))
