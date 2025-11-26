import requests
from faker import Faker
import time
import random
import string

# =======================================================================
# === 🚨 الخطوة 1: رابط الهدف (يجب استبدال الـ PLACEHOLDER) 🚨 ===
# =======================================================================

# استبدل هذا بعنوان URL الفعلي الذي تم تجميعه
TARGET_URL = "https://ladypopular.com/ajax/user.php"

# =======================================================================
# === 🚨 الخطوة 2: أسماء الحقول (يجب استبدال الـ PLACEHOLDER) 🚨 ===
# =======================================================================

FIELD_USERNAME = "reg_user"
FIELD_PASSWORD = "reg_pass"
FIELD_EMAIL = "reg_email"
FIELD_TERMS = "reg_terms"
FIELD_PRIVACY = "reg_privacy"
FIELD_MARKETING = "marketing-consent-choice"

# =======================================================================

fake = Faker()

def generate_user_data_logic():
    """توليد البيانات: اسم المستخدم هو نفسه كلمة المرور"""
    chars = string.ascii_lowercase + string.digits
    base_name = ''.join(random.choice(chars) for _ in range(8))
    
    username = base_name
    password = base_name
    
    email = fake.user_name() + str(random.randint(1, 999)) + "@" + fake.domain_name()
    
    return username, password, email

def register_account(session, username, password, email):
    """إرسال طلب POST لتسجيل حساب جديد"""
    
    # حمولة البيانات الكاملة
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
            print(f"✅ نجاح: تم تجنيد حساب جديد. بيانات الدخول:")
            print(f"    - اسم المستخدم (Username): {username}")
            print(f"    - كلمة المرور (Password): {password}")
            print("-" * 30)
            return True
        else:
            print(f"❌ فشل التسجيل لـ {username} | الحالة: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"⛔ خطأ في الاتصال لـ {username}: {e}")
        return False

def main_recruitment_loop(count=50):
    """حلقة التجنيد الرئيسية"""
    print(f"--- بدء عملية تجنيد {count} حسابات وهمية ---")
    session = requests.Session()
    
    for i in range(count):
        username, password, email = generate_user_data_logic()
        register_account(session, username, password, email)
        time.sleep(random.uniform(2.5, 5.0)) 
        
    print("--- انتهاء العملية. ---")

if __name__ == "__main__":
    main_recruitment_loop(count=50)
