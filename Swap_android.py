from requests import Session
from threading import Thread 
from ctypes import windll
from os import  system,kill,getpid
from signal import SIGTERM
from time import sleep
from uuid import uuid4

request_session =Session()

counters = 0 
error = 0 
RS = 0
proxies_list = []
def api_login():
        global authorization , username , target , User_Id
 
        username = input(" enter username: ")
        password = input(" enter password: ")
        target = input(" enter target: ")

        login_url = 'https://i.instagram.com/api/v1/accounts/login/'
    
        headers_login = {

            'X-Ig-Www-Claim': '0',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv10=',
            'User-Agent': 'Instagram 219.0.0.12.117 Android (25/7.1.2; 240dpi; 1280x720; samsung; SM-G977N; beyond1q; qcom; en_US; 346138365)',
            'Accept-Language': 'en-US',
            'X-Mid': 'YjKpKwABAAEBChfhQ0jDY79zjPt4',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': '674',
            'Accept-Encoding': 'gzip, deflate'
            }
            
        login_data = {

            'username': username,
            'enc_password': f"#PWD_INSTAGRAM:0:&:{password}",
            "adid":uuid4(),
            "guid":uuid4(),
            "device_id":uuid4(),
            "google_tokens":"[]",
            "phone_id":uuid4(),
            "login_attempt_count":"0"
            }

        req_login = request_session.post(url=login_url, headers=headers_login, data=login_data)
        if 'logged_in_user' in req_login.text:
            print(f"[+] Logged in with {username}")
            authorization = req_login.headers.get('ig-set-authorization')
            User_Id =  req_login.headers.get('Ig-Set-Ig-U-Ds-User-Id')
            info_swap()

        elif "challenge_required" in req_login.text:
            print(f"{username} is secured")
            api_login()

        else:
            print(req_login.text)
            api_login()
           
def info_swap():
    global email , phone_number , biography , full_name , external_url 
    url_info_swap='https://i.instagram.com/api/v1/accounts/current_user/?edit=true'
    headers_info_swap={
    
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US",
        "User-Agent": "Instagram 219.0.0.12.117 Android (25/7.1.2; 240dpi; 720x1280; samsung; SM-G977N; beyond1q; qcom; en_US; 346138365)",
        "X-IG-Capabilities": "3brTv10=",
        "X-IG-Connection-Type": "WIFI",
        "Authorization":authorization ,
        'X-Mid': 'YjKpKwABAAEBChfhQ0jDY79zjPt4',
        'Ig-U-Ds-User-Id': User_Id ,
        "X-Ig-Www-Claim": 'hmac.AR1g8KGN19_ZbpBkUHmFmFaTH5lqpK18LVH5eme7rO5rOZwr'
        }

    req_info_swap = request_session.get(url=url_info_swap,headers=headers_info_swap)
    # print(req_info_swap.text)

    if "pk" in req_info_swap.text and '"status":"ok"' in req_info_swap.text:
        email = req_info_swap.json()['user']['email']
        full_name = req_info_swap.json()['user']['full_name']
        phone_number = req_info_swap.json()['user']['phone_number']
        biography = req_info_swap.json()['user']['biography']
        external_url = req_info_swap.json()['user']['external_url']

    elif   "You've Been Logged Out" in req_info_swap.text:
        print("You've Been Logged Out, Please log back in")
        
    else:
        input(req_info_swap.text)
  
def swap():
    global counters , error

    try:

        url ='https://i.instagram.com/api/v1/accounts/edit_profile/'


        headers_info_swaper={

            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 219.0.0.12.117 Android (25/7.1.2; 240dpi; 720x1280; samsung; SM-G977N; beyond1q; qcom; en_US; 346138365)",
            "X-IG-Capabilities": "3brTv10=",
            "X-IG-Connection-Type": "WIFI",
            "Authorization":authorization ,
            'X-Mid': 'YhbJEgABAAGwrbrJ_HMZO9tApZsv',
            'Ig-U-Ds-User-Id': User_Id ,
            "X-Ig-Www-Claim": 'hmac.AR1yLMmQge1hvkcG8lv14PHICym-6t1PV46vtioqmGyXJPQY',
            "Ig-Intended-User-Id": User_Id

            }

        data = {
            "primary_profile_link_type":"0",
            "external_url":external_url,
            "phone_number":phone_number,
            "username":target,
            "show_fb_link_on_profile":"false",
            "first_name":full_name,
            "_uid":uuid4(),
            "device_id":uuid4(),
            "biography":biography,
            "_uuid":uuid4(),
            "email":email
            }
        
        for threads in range(CountsThread):
            req_swapper = request_session.post(url=url,headers=headers_info_swaper,data=data)
            if '"status":"ok"' in req_swapper.text:
                print(f"swapped @{target}")
                windll.user32.MessageBoxW(None,f"Successfully Swapped: @{target}\n\nAttempts: {counters}",'Swapper By @ikni')
                killed()

            elif "This username isn't available" in req_swapper.text: #status_code == 400
                # print(f'Swapping The Username: @{target} Attempts: {counters}')
                counters +=1

            elif "Please wait a few minutes before you try again." in req_swapper.text: #status_code == 429
                #print("too many requests")
                error +=1
            elif "Try Again Later" in req_swapper.text:
                error +=1

            else:
                pass
                # print(req_swapper.text)
    except:
        pass

def Threads():
    thread_list = []
    while True:
        for threads in range(CountsThread):
            target_swap = Thread(target=swap,daemon=True)
            target_swap.start()
            thread_list.append(target_swap)
        for count in thread_list:
            count.join()
def counter():  
    while True:
        before = counters 
        sleep(1)
        after = counters 
        RS = after-before
        system(f"title Attempts:{[counters]} R/L:{[error]} R/S:{[RS]}")

def killed():
    kill(getpid(), SIGTERM)

def starter():
    global CountsThread

    api_login()

    CountsThread= int(input("\n[ + ] Enter Your Thread: "))
    input("\n[ + ] Enter To Start: ")
    Thread(target=counter).start()
    Threads()

if __name__ == "__main__":
    starter()
    