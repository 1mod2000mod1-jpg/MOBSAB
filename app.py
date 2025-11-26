from flask import Flask, render_template_string, redirect, url_for
import requests
from faker import Faker
import time
import random
import string
import os 

app = Flask(__name__)

# =============================================================
# === 🚨 نقطة التفعيل النهائية: يجب تعديلها يدوياً على GitHub 🚨 ===
# =============================================================

# 1. الرابط الذي تم جمعه (يجب استبداله): https://ladypopular.com/ajax/user.php
TARGET_POST_URL = "https://ladypopular.com/ajax/user.php"
# 2. رابط صفحة التسجيل (للحصول على الكوكيز/الجلسة)
REGISTRATION_PAGE_URL = "https://ladypopular.com/"

# 3. أسماء الحقول الحقيقية التي تم جمعها:
FIELD_USERNAME = "reg_user"
FIELD_PASSWORD = "reg_pass"
FIELD_EMAIL = "reg_email"
FIELD_TERMS = "reg_terms"
FIELD_PRIVACY = "reg_privacy"
FIELD_MARKETING = "marketing-consent-choice"

# =============================================================

# الرؤوس التي تحاكي متصفح Chrome لمنع الاكتشاف
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': REGISTRATION_PAGE_URL # مهم جداً
}

fake = Faker()
RECRUITMENT_LOG = []
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

def generate_user_data_logic():
    """توليد البيانات: اسم المستخدم هو نفسه كلمة المرور"""
    chars = string.ascii_lowercase + string.digits
    base_name = ''.join(random.choice(chars) for _ in range(8))
    username = base_name
    password = base_name
    email = fake.user_name() + str(random.randint(1, 999)) + "@" + fake.domain_name()
    return username, password, email

def register_account(username, password, email):
    """عملية التسجيل المكونة من خطوتين (GET -> POST) لتجاوز الحماية"""
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # 1. خطوة التمهيد (GET): الحصول على الجلسة والكوكيز
    try:
        # زيارة رابط التسجيل للحصول على الكوكيز اللازمة للجلسة
        session.get(REGISTRATION_PAGE_URL, timeout=15)
    except requests.exceptions.RequestException as e:
        log_entry = f"⛔ خطأ في التمهيد/GET: {e}"
        RECRUITMENT_LOG.insert(0, log_entry)
        return

    # حمولة البيانات الكاملة
    payload = {
        FIELD_USERNAME: username,
        FIELD_PASSWORD: password,
        FIELD_EMAIL: email,
        FIELD_TERMS: '1',     
        FIELD_PRIVACY: '1',   
        FIELD_MARKETING: '1', 
        # يمكن إضافة أي توكنات مخفية تم العثور عليها هنا
    }
    
    # 2. خطوة التنفيذ (POST): إرسال البيانات
    try:
        response = session.post(TARGET_POST_URL, data=payload, timeout=15)
        
        # تحليل الاستجابة
        if response.status_code == 200 and ("success" in response.text.lower() or "ok" in response.text.lower()):
            log_entry = f"✅ نجاح: {username} | الباسوورد: {password}"
            RECRUITMENT_LOG.insert(0, log_entry) 
        else:
            log_entry = f"❌ فشل: {username} | الحالة: {response.status_code}. الرد: {response.text[:50]}..."
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
    return redirect(url_for('index'))

if __name__ == '__main__':
    # الاستماع إلى البورت المحدد بواسطة متغير بيئة Render
    port = int(os.environ.get('PORT', 8080)) 
    app.run(host='0.0.0.0', port=port)
