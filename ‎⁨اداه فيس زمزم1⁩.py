#تم فك من تيربو ادعيلي باجر ورايه امتحان كلش صعبب

import os
import sys
import time
import random
import requests
from datetime import datetime
from colorama import init, Fore, Style
from pyfiglet import Figlet

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION - الإعدادات
# ═══════════════════════════════════════════════════════════════════

# Initialize colorama
init(autoreset=True)

# Password verification
EXPECTED_PASSWORD = 'الحمدلله'

# ID generation settings
ID_PREFIX = '1000'
ID_TOTAL_LENGTH = 15
SLEEP_SECONDS = 1

# Checkpoint settings - نقاط إرسال التقارير
CHECKPOINTS = {250, 377, 500, 777, 1000, 1250, 1500, 2000}

# Color scheme - نظام الألوان
COLOR_ASCII = [
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.BLUE,
    Fore.RED
]
COLOR_PREFIX = Fore.YELLOW
COLOR_TEXT = Fore.WHITE
COLOR_ID = Fore.CYAN
COLOR_INFO = Fore.BLUE
COLOR_OK = Fore.GREEN
COLOR_ERROR = Fore.RED

# Telegram retry settings
TELEGRAM_RETRIES = 3
RETRY_BACKOFF_BASE = 1.5

# ASCII Art Banner
ASCII_ART = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⠶⠶⠶⠶⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠛⠁⠀⠀⠀⠀⠀⠀⠈⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⣠⡴⠞⠛⠉⠉⣩⣍⠉⠉⠛⠳⢦⣄⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⣴⡿⣧⣀⠀⢀⣠⡴⠋⠙⢷⣄⡀⠀⣀⣼⢿⣦⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⡾⠋⣷⠈⠉⠉⠉⠉⠀⠀⠀⠀⠉⠉⠋⠉⠁⣼⠙⢷⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣇⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣹⣆⠀⢻⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡟⠀⣰⣏⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠞⠋⠁⠙⢷⣄⠙⢷⣀⠀⠀⠀⠀⠀⠀⢀⡴⠋⢀⡾⠋⠈⠙⠻⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠹⢦⡀⠙⠳⠶⢤⡤⠶⠞⠋⢀⡴⠟⠀⠀⠀⠀⠀⠀⠙⠻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⠋⠀⠀⢀⣤⣤⣤⣤⣤⣤⣤⣿⣦⣤⣤⣤⣤⣤⣤⣴⣿⣤⣤⣤⣤⣤⣤⣤⡀⠀⠀⠙⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⠏⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⢠⣴⠞⠛⠛⠻⢦⡄⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠸⣇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⡟⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⣿⣿⢶⣄⣠⡶⣦⣿⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣾⠁⠀⠀⠀⠀⠘⣇⠀⠀⠀⠀⠀⠀⠀⢻⣿⠶⠟⠻⠶⢿⡿⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠈⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢰⡏⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⢾⣄⣹⣦⣀⣀⣴⢟⣠⡶⠀⠀⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⣭⣭⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⢿⡀⠀⠀⠀⠀⠀⠀⣀⡴⠞⠋⠙⠳⢦⣀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⢰⡏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⢿⣄⣀⠀⠀⢀⣤⣼⣧⣤⣤⣤⣤⣤⣿⣭⣤⣤⣤⣤⣤⣤⣭⣿⣤⣤⣤⣤⣤⣼⣿⣤⣄⠀⠀⣀⣠⡾⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠻⢧⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠼⠟⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿تم الفك من تيربو ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣶⣿⣿
"""


# ═══════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS - الدوال المساعدة
# ═══════════════════════════════════════════════════════════════════

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def term_width():
    """Get terminal width with fallback"""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def print_centered(text, color=Fore.WHITE):
    """Print text centered on screen"""
    w = term_width()
    for line in text.splitlines():
        print(color + line.center(w))


def print_big_text(text, color=Fore.WHITE, font='slant'):
    """Print big ASCII text centered"""
    f = Figlet(font=font)
    art = f.renderText(text)
    w = term_width()
    for line in art.splitlines():
        print(color + Style.BRIGHT + line.center(w))


def mask_sensitive(value: str, keep: int = 4) -> str:
    """Mask sensitive information showing only first and last characters"""
    if not value:
        return ''
    if len(value) <= keep * 2:
        if len(value) <= 2:
            return '*' * len(value)
        return value[0] + ('*' * (len(value) - 2)) + value[-1]
    return value[:keep] + ('*' * (len(value) - keep * 2)) + value[-keep:]


def generate_fake_id(prefix=ID_PREFIX, total_length=ID_TOTAL_LENGTH):
    """Generate a fake Instagram-like ID"""
    suffix_len = max(0, total_length - len(prefix))
    suffix = ''.join(random.choice('0123456789') for _ in range(suffix_len))
    return prefix + suffix


def dynamic_separator(char='―'):
    """Create dynamic separator based on terminal width"""
    return char * max(10, term_width() - 10)


def build_report(checked_id: str, fake_pass: str, count: int):
    """Build report message for Telegram"""
    creation_date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    
    msg = f"""📣 تقرير فحص حساب

--------------------------------
الحساب الذي تم فحصه: {checked_id}
كلمة المرور: {fake_pass}
تاريخ صيد: {creation_date}
--------------------------------
عدد الفحوصات حتى الآن: {count}
حقوق: @Turbo1D | قنوات المطور
"""
    return msg


# ═══════════════════════════════════════════════════════════════════
# TELEGRAM FUNCTIONS - دوال التلجرام
# ═══════════════════════════════════════════════════════════════════

def send_telegram(bot_token: str, chat_id: str, text: str):
    """Send message to Telegram with retry logic"""
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    headers = {'Content-Type': 'application/json'}
    
    attempt = 0
    while attempt < TELEGRAM_RETRIES:
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            if resp.status_code == 200:
                return True
            print(COLOR_ERROR + f'[تحذير] استجابة التلجرام: {resp.status_code} - {resp.text}')
        except Exception as e:
            print(COLOR_ERROR + f'[خطأ] محاولة إرسال فشلت: {e}')
        
        attempt += 1
        wait = int(RETRY_BACKOFF_BASE ** attempt)
        print(COLOR_INFO + f'إعادة المحاولة بعد {wait} ثانية... (محاولة {attempt + 1})')
        time.sleep(wait)
    
    return False


def validate_telegram_credentials(bot_token: str, chat_id: str):
    """Validate Telegram bot token and chat ID"""
    # Validate bot token
    me_url = f'https://api.telegram.org/bot{bot_token}/getMe'
    try:
        r = requests.get(me_url, timeout=8)
        if r.status_code != 200:
            print(COLOR_ERROR + f'[خطأ] توكن غير صالح أو مشكلة اتصال: {r.status_code} - {r.text}')
            return False
    except Exception as e:
        print(COLOR_ERROR + f'[خطأ] فشل التحقق من التوكن: {e}')
        return False
    
    # Validate chat ID
    chat_url = f'https://api.telegram.org/bot{bot_token}/getChat'
    try:
        r = requests.post(chat_url, json={'chat_id': chat_id}, timeout=8)
        if r.status_code != 200:
            print(COLOR_ERROR + f'[تحذير] فحص chat_id أعطى: {r.status_code} - {r.text}')
            return False
    except Exception as e:
        print(COLOR_ERROR + f'[تحذير] لم نتمكن من فحص chat_id: {e}')
        return False
    
    return True


# ═══════════════════════════════════════════════════════════════════
# MAIN FUNCTION - الدالة الرئيسية
# ═══════════════════════════════════════════════════════════════════

def main():
    """Main application logic"""
    clear_screen()
    color_idx = 0
    print_centered(ASCII_ART, color=COLOR_ASCII[color_idx % len(COLOR_ASCII)])
    time.sleep(0.4)
    print_big_text('@Turbo1D', color=COLOR_ASCII[(color_idx + 1) % len(COLOR_ASCII)])
    color_idx += 2
    
    # Password verification
    verify_pw = input(Style.BRIGHT + COLOR_TEXT + 'ادخل كلمة التحقق لتشغيل الأداة: ').strip()
    if verify_pw != EXPECTED_PASSWORD:
        print(COLOR_ERROR + 'كلمة التحقق غير صحيحة. الخروج.')
        sys.exit(1)
    
    # Get Telegram credentials
    tg_chat_id = input(COLOR_TEXT + 'ادخل ايدي حسابك على تلجرام (chat_id): ').strip()
    tg_bot_token = input(COLOR_TEXT + 'ادخل توكن بوت التلجرام (bot token): ').strip()
    if not tg_chat_id or not tg_bot_token:
        print(COLOR_ERROR + 'يجب إدخال chat_id و bot token للمتابعة. الخروج.')
        sys.exit(1)
    
    # Validate credentials
    print(COLOR_INFO + 'التحقق من بيانات التلجرام (token/chat_id)...')
    if not validate_telegram_credentials(tg_bot_token, tg_chat_id):
        print(COLOR_ERROR + "فشل التحقق من بيانات التلجرام. تابع رغم ذلك؟ اكتب 'y' للاستمرار أو أي مفتاح للخروج.")
        cont = input().strip().lower()
        if cont != 'y':
            print(COLOR_OK + 'إنهاء.')
            sys.exit(1)
        else:
            print(COLOR_INFO + 'المتابعة حسب رغبتك — قد تفشل الإرسالات إذا كانت البيانات خاطئة.')
    
    # Mask sensitive data for display
    masked_chat_id = mask_sensitive(tg_chat_id, keep=4)
    masked_token = mask_sensitive(tg_bot_token, keep=4)
    
    counter = 0
    reports_sent = 0
    last_id = None
    
    try:
        while True:
            counter += 1
            fake_id = generate_fake_id()
            last_id = fake_id
            fake_pass = 'zz' + str(random.randint(1000, 9999999))
            
            # Update color
            color = COLOR_ASCII[color_idx % len(COLOR_ASCII)]
            clear_screen()
            print_centered(ASCII_ART, color=color)
            print_big_text('@Turbo1D', color=COLOR_ASCII[(color_idx + 1) % len(COLOR_ASCII)])
            color_idx += 1
            
            # Display separator
            sep = dynamic_separator()
            print(Style.BRIGHT + Fore.MAGENTA + sep + '\n')
            
            # Display check info
            prefix = f'[{counter}] '
            label = 'تم العثور آيدي: '
            tail = ' — جار فحص الحساب...'
            print(
                Style.BRIGHT + COLOR_PREFIX + prefix +
                Style.NORMAL + COLOR_TEXT + label +
                Style.BRIGHT + COLOR_ID + fake_id +
                Style.NORMAL + COLOR_TEXT + tail + '\n'
            )
            
            print(Style.DIM + Fore.WHITE + 'معرّف التليجرام (مقنع): ' + Style.BRIGHT + Fore.GREEN + masked_chat_id)
            print(Style.DIM + Fore.WHITE + 'توكن البوت (مقنع): ' + Style.BRIGHT + Fore.MAGENTA + masked_token + '\n')
            
            # Check if should send report
            should_send = False
            if counter in CHECKPOINTS:
                should_send = True
            elif counter >= max(CHECKPOINTS) and counter % 250 == 0:
                should_send = True
            
            if should_send:
                report_text = build_report(checked_id=fake_id, fake_pass=fake_pass, count=counter)
                print(COLOR_INFO + f'[ارسال] إرسال تقرير إلى التلجرام (عدد={counter}) ...')
                ok = send_telegram(tg_bot_token, tg_chat_id, report_text)
                if ok:
                    reports_sent += 1
                    print(COLOR_OK + '[نجاح] تم إرسال التقرير.\n')
                else:
                    print(COLOR_ERROR + '[فشل] لم يتم إرسال التقرير — تحقق من التوكن/chat_id أو اتصال الانترنت.\n')
            
            # Display statistics
            stats = f'الإحصاءات: الفحوصات={counter} | تقارير مُرسلة={reports_sent} | آخر آيدي={last_id}'
            print(Style.DIM + Fore.WHITE + stats + '\n')
            
            time.sleep(SLEEP_SECONDS)
            
    except KeyboardInterrupt:
        print(COLOR_OK + '\nتم إيقاف الأداة بواسطة المستخدم. إلى اللقاء.')
        print(Style.BRIGHT + Fore.WHITE + f'ملخص: إجمالي فحوصات = {counter}, تقارير أرسلت = {reports_sent}')
        sys.exit(0)
    except Exception as e:
        print(COLOR_ERROR + f'\n[خطأ غير متوقع] {e}')
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════
# ENTRY POINT - نقطة الدخول
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    main()