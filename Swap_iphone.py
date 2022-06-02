from requests import Session
from threading import Thread
from ctypes import windll
from random import choice
from os import  system,kill,getpid
from signal import SIGTERM
from time import sleep
from uuid import uuid4  # uuid4 is to create a random uuid to bypass block login in instagram

requests_session = Session()  # to keep your login alive 

counters = 0 
error = 0 
RS = 0
proxies_list = []

def login():
    global target , session_id , get_csrftoken, target
    username = input("\n\nEnter Your username: ")
    password = input("\nEnter Your password: ")
    target= input("\n[ + ] Enter Your target: ")

    url_login = "https://i.instagram.com/api/v1/accounts/login/"
    header_login = {

        "Host": "i.instagram.com",
        "X-Ig-Connection-Type": "WiFi",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Ig-Capabilities": "36r/Fx8=",
        "User-Agent": "Instagram 159.0.0.28.123 (iPhone8,1; iOS 14_1; en_SA@calendar=gregorian; ar-SA; scale=2.00; 750x1334; 244425769) AppleWebKit/420+",
        "X-Ig-App-Locale": "en",
        "X-Mid": "Ypg64wAAAAGXLOPZjFPNikpr8nJt",
        "Content-Length": "778",
        "Accept-Encoding": "gzip, deflate"
        }

    data_login = {

        "username":username,
        "reg_login":"0",
        "enc_password":f"#PWD_INSTAGRAM:0:&:{password}",
        "device_id":uuid4(),
        "login_attempt_count":"0",
        "phone_id":uuid4()
        }

    req_login = requests_session.post(url=url_login,headers=header_login,data=data_login)
    if 'logged_in_user' in req_login.text:
        print(f"[+] Logged in with {username}")
        session_id = req_login.cookies.get("sessionid")
        user_id = req_login.cookies.get("ds_user_id")
        get_csrftoken = req_login.cookies.get("csrftoken")
        info_swap()
    
    elif 'The password you entered is incorrect' in req_login.text:
        print("The password you entered is incorrect\n\n")
        login()

    elif "The username you entered doesn't appear to belong to an account" in req_login.text:
        print(f"{username} Not Found\n\n")
        login()

    elif "challenge_required" in req_login.text:
        print(f"{username} is secured")
        login()
    
    elif "Try Again Later" in req_login.text:
        print(f"Blocked login Try Again Later")
        login()

    else:
        input(f"\n\n{req_login.text}")
        login()


def info_swap():
    global username ,email , phone_number , biography , full_name , external_url  
   
    url_info_swap='https://i.instagram.com/api/v1/accounts/current_user/?edit=true'
    headers_info_swap={

        'User-Agent': 'Instagram 159.0.0.28.123 (iPhone8,1; iOS 14_1; en_SA@calendar=gregorian; ar-SA; scale=2.00; 750x1334; 244425769) AppleWebKit/420+',
        'Connection': 'Keep-Alive', 
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate' ,
        'X-Ig-Www-Claim': 'hmac.AR3pOL5xyu1Rks73Bf0LiqE4TekMNX3UuKCvHfEyVCP-iw1S',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Ig-Capabilities': '36r/Fx8=',
        'X-Ig-Connection-Type': 'WiFi',
        'Host': 'i.instagram.com',
        'Cookie': f'sessionid={session_id}'
        }


    req_info_swap = requests_session.get(url=url_info_swap,headers=headers_info_swap)
    if "pk" in req_info_swap.text and '"status":"ok"' in req_info_swap.text:
        email = req_info_swap.json()['user']['email']
        full_name = req_info_swap.json()['user']['full_name']
        phone_number = req_info_swap.json()['user']['phone_number']
        biography = req_info_swap.json()['user']['biography']
        external_url = req_info_swap.json()['user']['external_url']
        username = req_info_swap.json()["user"]["username"]

    elif req_info_swap.status_code==403:
        input(f"\nBad Sessionid {session_id}")
        killed()

    elif "challenge_required" in req_info_swap.text:
        input(f"\n\nsecured...! ")
        killed()
    else:
        input(req_info_swap.text)
        killed()

def swapper():

    global counters , error
       
    try:
        url='https://i.instagram.com/api/v1/accounts/edit_profile/'

        header={
            'User-Agent': 'Instagram 159.0.0.28.123 (iPhone8,1; iOS 14_1; en_SA@calendar=gregorian; ar-SA; scale=2.00; 750x1334; 244425769) AppleWebKit/420+',
            'Connection': 'Keep-Alive', 
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate' ,
            'X-Ig-Www-Claim': 'hmac.AR24BNL0FIyXEZ_HsY5tzVhiVWFEycjqTifRIGsgJt5KoAQt',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Ig-Capabilities': '36r/Fx8=',
            'X-Ig-Connection-Type': 'WiFi',
            'Host': 'i.instagram.com',
            'Cookie': f'sessionid={session_id}'
            }

        data={
            'username': target,
            "_csrftoken":get_csrftoken,
            "_uuid":uuid4(),
            "device_id":uuid4(),
            "email":email,
            "phone_number":phone_number,
            "first_name":full_name,
            }
        for threads in range(CountsThread):

            req_sessions_login = requests_session.post(url=url,headers=header,data=data,proxies=random_proxy(),timeout=2)

            if '"status":"ok"' in req_sessions_login.text:
                print(f"swapped @{target}")
                windll.user32.MessageBoxW(None,f"Successfully Swapped: @{target}\n\nAttempts: {counters}",'Swapper By @ikni')
                killed()

            elif "This username isn't available" in req_sessions_login.text:
                # print(f'Swapping The Username: @{target} Attempts: {counters}')
                counters +=1
                
            elif req_sessions_login.status_code==429 or "Try Again Later" in req_sessions_login.text:
                error +=1
                
            else:
                print(req_sessions_login.text)              
    except:
        pass

def Thread_swapper():
    thread_list = []
    while True:
        for threads in range(CountsThread):
            target_swap = Thread(target=swapper,daemon=True)
            target_swap.start()
            thread_list.append(target_swap)
        for count in thread_list:
            count.join()

def random_proxy():
    for file in proxies_file:
        proxies_list.append(file)
    proxies_choice = choice(proxies_list)
    proxy = {"http": f"socks4://{proxies_choice}", "https": f"socks4://{proxies_choice}"}
    requests_session.proxies.update(proxy) # it uses just proxies work 
    return proxy

def killed():
    kill(getpid(), SIGTERM)

def counter():
    
    while True:
        before = counters 
        sleep(1)
        after = counters 
        RS = after-before
        system(f"title Attempts:{[counters]} R/L:{[error]} R/S:{[RS]}")

def starter():
    global proxies_file , CountsThread

    try:
        proxies_file = list(open(f"proxies.txt", "r").read().split("\n"))
        if len(proxies_file) < 1:
            input("proxies file is empty !")
        counts_proxies = sum(1 for line in open('proxies.txt'))
        print(f"\n{counts_proxies} proxies.txt")
        login()
    except FileNotFoundError:
        url = requests_session.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt")
        url1 = requests_session.get("https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt")
        url2 = requests_session.get("https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt")
        url3 = requests_session.get("https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt")
        #
        file_text = open("proxies.txt", "a")
        file_text.write(url.text.replace('\n\n', ''))
        file_text.write(url1.text.replace('\n\n', ''))
        file_text.write(url2.text.replace('\n\n', ''))
        file_text.write(url3.text.replace('\n\n', ''))
        counts_file = sum(1 for line in open('proxies.txt'))
        print(f"\n{counts_file} proxies.txt")
        login()

    CountsThread= int(input("\n[ + ] Enter Your Thread: "))
    input("\n[ + ] Enter To Start: ")
    Thread(target=counter).start()
    Thread_swapper()

if __name__ == "__main__":
    starter()