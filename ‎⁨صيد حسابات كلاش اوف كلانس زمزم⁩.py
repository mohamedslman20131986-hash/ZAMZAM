import requests, random, time, os, string

# الوان
R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
C = "\033[1;36m"
W = "\033[1;37m"

os.system("clear")
print(R + "☠️ أداة صيد حسابات كلاش اوف كلانس (☠️")
print(G + "بواسطة: الشـبـح | @a_YDs\n")

# إدخال التوكن والآيدي
token = input(Y + "[+] أدخل توكن البوت: " + W)
chat_id = input(Y + "[+] أدخل ID التليجرام: " + W)

def generate_name(length=3):
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))

def send_to_bot(name, email):
    message = f"""
- 𝑵𝑬𝑾 𝑨𝑪𝑪𝑶𝑵𝑼𝑻 -

   𝑵𝑨𝑴𝑬🤫 {name}

𝒆𝒎𝑨𝒊𝒍😈 {email}

  𝒑𝒚☞ @a_YDs
  𝒑𝒖 𝒈𝒓𝒐𝒑 @pyshonvip
"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})

# توليد حسابات  ذكية
while True:
    name = generate_name(3)
    email = name.lower() + "@yopmail.com"

    print(C + f"[+] تم صيد حساب: {email}")
    send_to_bot(name, email)
    time.sleep(2)