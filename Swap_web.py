from requests import Session
from os import system , getpid , kill
from threading import Thread 
from time import sleep
from ctypes import windll
from signal import SIGTERM

#last update 29-5-2022

system(f"title Swapper By @ikni")

email = ""
first_name = ""
phone_number = ""
biography = ""
external_url = ""
get_sessions = ""
get_csrftoken = ""
target = ""
counters = 1

requests_sessions = Session()

# function to login in instagram
def login_web():
    global get_csrftoken , get_sessions , username , headers_login , url_login , req_login 

    username = input(f'\n\n[ + ] Enter Your Username: ')
    password = input(f'\n[ + ] Enter Your Password: ') 

    system('cls||clear')
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    headers_login = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,ar;q=0.8",
        "content-length": "317",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "ig_nrcb=1; mid=YpLcvgALAAFFRymO87zq19HVCPmf; ig_did=C898BD07-7DF1-4E64-9C32-C6FC8BEEEA25; csrftoken=oDHY582gXXWCy3x4Y3WIOKSIY7lfzjBR",
        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        "x-asbd-id": "198387",
        "x-csrftoken": "oDHY582gXXWCy3x4Y3WIOKSIY7lfzjBR",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR0j2Hx6v7zmyqZfkQL1eHJw5zx_e2z2ECz9jh-JVWCNBg3-",
        "x-instagram-ajax": "684510d5f3c6",
        "x-requested-with": "XMLHttpRequest"
        }

    #  Data for username
    data_login = {
        "username": f"{username}",
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:&:{password}",
        "queryParams": {},
        "optIntoOneTap": "false",
        "trustedDeviceRecords": {}
        }
   
    req_login = requests_sessions.post(url_login, headers=headers_login, data=data_login) # request for Account
    try:    
        # login Check for Account

        if '"user":true,"authenticated":false' in req_login.text:
            print(f'\n[ * ] Your Password Is Wrong ! Please Check Your Password\n\n')
            login_web()

        elif '"checkpoint_required"' in req_login.text:
            print(f"@{username} Is Secured ! Please Activate Your code To login\n\n")
            login_web()

        elif '"feedback_required"' in req_login.text:
            print(f"[ * ] Rate Limited. Please wait a few minutes. ")
            login_web()
        
        elif '"two_factor_required":true' in req_login.text:
            print(f"@{username} Has Two Factor authentication\nPlease Turn It Off And Try Again\n\n")
            login_web()
        
        elif '"user":false,"authenticated":false' in req_login.text:
            print(f'@{username} not found\n\n')
            login_web()
        
        elif "Please wait a few minutes before you try again" in req_login.text:
            print(f"[ * ] Rate Limited. Please wait a few minutes. ")
            login_web()

        elif '"authenticated":true' in req_login.text:
            print(f'@{username} Logged In √ \n')
            get_sessions = req_login.cookies['sessionid']
            get_csrftoken = req_login.cookies.get_dict()['csrftoken']
            method()

        elif "We've updated our Terms, and need you to agree to them before continuing to use Instagram." in req_login.text:
            print(f"[ * ] login Your account in broswer and agree Instagram Terms please")
            login_web()
        
        elif "screen_key" in req_login.text:
            print(f"[ * ] login Your account in broswer and choose your age please")
            login_web()

        elif "Your account has been permanently disabled because it didn't follow our Community Guidelines." in req_login.text:
            print(f"[ * ] {username} is deleted because passed 30 days")
            login_web()

        elif '"status":"fail"' in req_login.text:
            print(f"[ * ] We couldn't connect to Instagram. Make sure you're connected to the internet and try again.")
            login_web()

        elif "Help Us Confirm You Own This Account" in req_login.text:
            print("Help Us Confirm You Own This Account")

        else: 
            print(req_login.text)
            login_web()

    except ValueError:
        print(req_login.text)
        input(f"[ ! ] Excepted Error ! Check On Your Username And Password")
        exit()

# function to get info swap for account
def info_swap():
    global email , phone_number , biography , first_name , external_url 

    url_info_swap = 'https://www.instagram.com/accounts/edit/?__a=1&__d=dis'
    headers_info_swap = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'cookie': f"ig_nrcb=1; mid=YpLcvgALAAFFRymO87zq19HVCPmf; ig_did=C898BD07-7DF1-4E64-9C32-C6FC8BEEEA25; csrftoken={get_csrftoken}; sessionid={get_sessions};",
        'referer': f'https://www.instagram.com/{username}/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
        "x-asbd-id": "198387",
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR0j2Hx6v7zmyqZfkQL1eHJw5zx_e2z2ECz9jh-JVWCNBg3-',
        'x-requested-with': 'XMLHttpRequest'
        }

    req_info_swap = requests_sessions.get(url_info_swap, headers=headers_info_swap)
    email = str(req_info_swap.json()['form_data']['email'])
    first_name = str(req_info_swap.json()['form_data']['first_name'])
    phone_number = str(req_info_swap.json()['form_data']['phone_number'])
    biography = str(req_info_swap.json()['form_data']['biography'])
    external_url = str(req_info_swap.json()['form_data']['external_url'])

    if '"is_email_confirmed":false' in req_info_swap.text:
        input(f"{email} please confirm your email before swapping")
        exit()

# function to swapping account
def swap_username():
    global counters

    url_swap_username = 'https://www.instagram.com/accounts/edit/'
    headers_swap_username = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'content-length': '115',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f"ig_nrcb=1; mid=YpLcvgALAAFFRymO87zq19HVCPmf; ig_did=C898BD07-7DF1-4E64-9C32-C6FC8BEEEA25; csrftoken={get_csrftoken}; sessionid={get_sessions}",
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/edit/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
        "x-asbd-id": "198387" ,
        'x-csrftoken': get_csrftoken,
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR0j2Hx6v7zmyqZfkQL1eHJw5zx_e2z2ECz9jh-JVWCNBg3-',
        'x-instagram-ajax': '684510d5f3c6',
        'x-requested-with': 'XMLHttpRequest',
        }

    data_swap_username = {
        'first_name': first_name,
        'email': email,
        'username': target,
        'phone_number': phone_number,
        'biography': biography,
        'external_url': external_url,
        'chaining_enabled': 'on'
        }
    
    req_swap_username = requests_sessions.post(url_swap_username, data=data_swap_username, headers=headers_swap_username)
    try:

        if '"status":"ok"' in req_swap_username.text: 
            print(f'Swapped To: @{target}')
            windll.user32.MessageBoxW(None,f"Successfully Swapped: @{target}\n\nAttempts: {counters}",'Swapper By @ikni')
            killed()

        elif  "This username isn't available" in req_swap_username.text:
            print(f'Swapping The Username: @{target} Attempts: {counters}')
            counters+=1

        elif '"Please wait a few minutes before you try again."' in req_swap_username.text:
            windll.user32.MessageBoxW(None,f"Your Account is Blocked Please wait a few minutes",'Swapper By @ikni')
            killed()
        
        elif "We restrict certain activity to protect our community." in req_swap_username.text:
            windll.user32.MessageBoxW(None,f"{username} is spam Try Again Later",'Swapper By @ikni')
            killed()

        else:
            pass              

    except:
        print(req_swap_username.text)
        windll.user32.MessageBoxW(None,f"ERROR SWAPPING !!!",'Swapper By @ikni')
        killed() 

def killed():

    kill(getpid(), SIGTERM)

def check_block():

    url_swap = 'https://www.instagram.com/accounts/edit/'
    headers_swap = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'content-length': '115',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f"ig_nrcb=1; mid=YpLcvgALAAFFRymO87zq19HVCPmf; ig_did=C898BD07-7DF1-4E64-9C32-C6FC8BEEEA25; csrftoken={get_csrftoken}; sessionid={get_sessions}",
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/edit/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
        "x-asbd-id": "198387" ,
        'x-csrftoken': get_csrftoken,
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR0j2Hx6v7zmyqZfkQL1eHJw5zx_e2z2ECz9jh-JVWCNBg3-',
        'x-instagram-ajax': '684510d5f3c6',
        'x-requested-with': 'XMLHttpRequest',
        }

    data_swap = {

        'first_name': first_name,
        'email': email,
        'username': username,
        'phone_number': phone_number,
        'biography': biography,
        'external_url': external_url,
        'chaining_enabled': 'on'
        }
    
    req_swap = requests_sessions.post(url_swap, data=data_swap, headers=headers_swap)

    if req_swap.status_code == 200:
        print(f"\n{username} Is Not Blocked You Can Swapping\n")

    elif req_swap.status_code == 429 or "Please wait a few minutes before you try again" in req_swap.text:
        print("Your account is Blocked Please wait a few minutes")
        login_web()
    
    elif "A user with that username already exists." in req_swap.text: # you can swap username, no has 14 days
        print("A user with that username already exists.")

    elif "We restrict certain activity to protect our community" in req_swap.text:
        print(f"Your {username} is Blocked Please Try Again Later")
        login_web()

    else:
        print(req_swap.text)
        login_web()


def method():
    global target,CountsThread 
    info_swap()
    sleep(1)
    check_blocked = input("Do you want to check the username (y) or (n): ")
    if check_blocked == ("y"):
        check_block()
    elif check_blocked == ('n') or ("") :
        pass
    else:
        pass
    
    target = input(f'\n[ + ] Enter Your Target: ')
    CountsThread= int(input(f"\n[ + ] Enter Your Thread: "))
    if CountsThread == "":
        CountsThread = int("1")
    windll.user32.MessageBoxW(None,f"Please Swapping Before 50 Attempts",'Swapper By @ikni')
    RunThread()

def RunThread():
    thread_list = []
    while True:
        for threads in range(CountsThread):
            target_swap = Thread(target=swap_username)
            target_swap.start()
            thread_list.append(target_swap)

        for count in thread_list:
            count.join()

if __name__ == "__main__":
    login_web()