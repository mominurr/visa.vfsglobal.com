try:
    import os,requests
    os.environ['WDM_PROGRESS_BAR'] = str(0)
    import traceback,sys,time
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import whisper
    import warnings
    import datetime
    from bs4 import BeautifulSoup as bs
    import smtplib
    from email.message import EmailMessage
except Exception as error:
    with open('module_error.txt','a+',encoding='utf-8') as file:
        file.write(f"{error}\n")
driver=None
# Record the start time
start_time = datetime.datetime.now()
warnings.filterwarnings("ignore")
model = whisper.load_model("base")
SENDER_EMAIL = "sender_email"
APP_PASSWORD = "sender_app_password"
headers = {
        "accept": "*/*",
        "accept-language": 'en-US,en;q=0.9',
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }


# free ssl proxy collect function

def get_sslproxies():
    retray=0
    while retray<3:
        try:
            urls = 'https://www.sslproxies.org/'
            res = requests.get(urls,headers=headers,timeout=10)
            soups = bs(res.text, 'html.parser')
            table_htmls=soups.find('div',attrs={'class':'table-responsive fpl-list'})
            tables = table_htmls.find('table')
            tbodys=tables.find('tbody')
            table_rows=tbodys.find_all('tr')
            proxie = []
            for rows in table_rows:
                column = rows.find_all('td')
                proxys = {'ip': column[0].text, 'port': column[1].text, 'code': column[2].text,
                        'country': column[3].text, 'anonymity': column[4].text, 'google': column[5].text,
                        'https': column[6].text, 'last_checked': column[7].text}
                proxie.append(proxys)
            proxies_lists=[]
            for lists in proxie:
                # if lists["https"]=="yes":
                #     proxies_lists.append(f"https://{lists['ip']}:{lists['port']}")
                # else:
                if lists["anonymity"]=="elite proxy":
                    proxies_lists.append(f"{lists['ip']}:{lists['port']}")
                    
            return proxies_lists
        except:
            retray+=1
            continue
    if retray>3:
        return None




# verify collected free proxy is working or not

def verify_proxy():
    proxy_lists=get_sslproxies()
    if proxy_lists is None:
        return None
    veryfy_proxy_lists=[]
    for proxy_ip in proxy_lists:
        url="https://ipinfo.io/json"
        proxies=f'http://{proxy_ip}'
        try:
            response=requests.get(url,headers=headers,proxies={"http": proxies},timeout=3)
            if response.status_code==200:
                # ip=response.json()['ip']
                # print(f"{response.status_code}: proxy_ip: {proxy_ip} : ip: {ip}")
                # if proxy_ip==ip:
                veryfy_proxy_lists.append(proxy_ip)
        except:
            pass
    if len(veryfy_proxy_lists)==0:
        return proxy_lists
    else:
        return veryfy_proxy_lists



# Email sending  afir9181@gmail.com

def send_mail(content):
    try:
        recipient_email='recipient_email'
        subject='Hello From Python Bot For Italy!'
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg.set_content(content)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
    except:
        sys.stderr = open('error.log', 'a+',encoding='utf-8')
        traceback.print_exc()
        sys.stderr.close()
        pass



#captcha recorded audio converted text 
def transcribe(url):
    try:
        with open('audio.mp3', 'wb') as f:
            f.write(requests.get(url).content)
        result = model.transcribe("audio.mp3")
        return result["text"].strip()
    except:
        sys.stderr = open('error.log', 'a+',encoding='utf-8')
        traceback.print_exc()
        sys.stderr.close()
        pass
    


# captcha checkbox button click
def click_checkbox(driver):
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor-label"))).click()
    except:
        sys.stderr = open('error.log', 'a+',encoding='utf-8')
        traceback.print_exc()
        sys.stderr.close()
        pass
    # driver.find_element(By.ID, "recaptcha-anchor-label").click()


# captcha audio button click
def request_audio_version(driver):
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))).click()
    except:
        sys.stderr = open('error.log', 'a+',encoding='utf-8')
        traceback.print_exc()
        sys.stderr.close()
        pass
    # driver.find_element(By.ID, "recaptcha-audio-button").click()


# get captcha audio source and verify captcha
def solve_audio_captcha(driver):
    try:
        src_url=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "audio-source"))).get_attribute('src')
        # src_url=driver.find_element(By.ID, "audio-source").get_attribute('src')
    except:
        src_url=""
    if len(src_url)!=0:
        try:
            text = transcribe(src_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "audio-response"))).send_keys(text)
            # driver.find_element(By.ID, "audio-response").send_keys(text)
            # driver.find_element(By.ID, "recaptcha-verify-button").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-verify-button"))).click()
        except:
            sys.stderr = open('error.log', 'a+',encoding='utf-8')
            traceback.print_exc()
            sys.stderr.close()
            pass
    else:
        try:
            driver.switch_to.default_content()
            driver.switch_to.parent_frame()
        except:
            pass
        return True
    try:
        error_message=driver.find_element(By.ID,"rc-audiochallenge-error-message").text.strip()
    except:
        error_message=''
    if len(error_message)!=0:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-reload-button"))).click()
            # driver.find_element(By.ID,"recaptcha-reload-button").click()
            time.sleep(3)
            solve_audio_captcha(driver)
        except:
            pass
    try:
        driver.switch_to.default_content()
        driver.switch_to.parent_frame()
    except:
        pass
    return False


# main controling function
def automation_function():
    driver=None
    try:
        proxy_lists=verify_proxy()
        print("len: ",len(proxy_lists))
    except:
        proxy_lists=None
    
    if proxy_lists is not None:
        for proxy_ip in proxy_lists:
            # print(proxy_ip)
            try:
                # random_user_agent = random.choice(user_agents)
                options = uc.ChromeOptions()
                options.add_argument("--excludeSwitches=enable-automation")
                options.add_argument("--excludeSwitches=enable-logging")
                options.add_argument('--lang=en-US')
                # options.add_argument(f"--user-agent={user_agent}")
                options.add_argument(f'--proxy-server={proxy_ip}')
                # options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')
                # options.add_argument(f'--proxy-auth={proxy_username}:{proxy_password}')
                options.add_argument("ignore-certificate-errors")
                options.add_argument('--headless')
                driver = uc.Chrome(options=options,version_main = 114)
                driver.set_page_load_timeout(100)
            except:
                sys.stderr = open('error.log', 'a+',encoding='utf-8')
                traceback.print_exc()
                sys.stderr.close()

            try:
                driver.get('https://visa.vfsglobal.com/gbr/en/ita/login')
                time.sleep(20)
            except:
                driver.close()
                time.sleep(5)
                continue
            try:
                # Record the end time
                end_time = datetime.datetime.now()
                # Calculate the time difference
                time_difference = end_time - start_time
                # Check if the time difference exceeds 30 minutes
                if time_difference.total_seconds() >= 28 * 60:
                    try:
                        driver.close()
                    except:
                        pass
                    exit()
            except:
                pass    
            try:
                error_text=driver.find_element(By.ID,'error-code').text.strip()
            except:
                error_text=''
            if len(error_text)!=0:
                try:
                    driver.close()
                    time.sleep(5)
                    continue
                except:
                    pass
            else:
                time.sleep(20)
                
            flag=False
            # cookies reject button click
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"onetrust-reject-all-handler"))).click()
                time.sleep(10)
            except:
                flag=True
                pass
            if flag:
                try:
                    driver.close()
                    time.sleep(5)
                    continue
                except:
                    pass
                
        
            Flag=False
            # recaptcha solve
            try:
                click_checkbox(driver)
                time.sleep(1)
                request_audio_version(driver)
                time.sleep(1)
                Flag=solve_audio_captcha(driver)
                # driver.switch_to.default_content()
                time.sleep(10)
            except:
                pass
            try:
                driver.switch_to.default_content()
            except:
                pass
            if Flag:
                try:
                    driver.close()
                    time.sleep(5)
                    continue
                except:
                    pass
            else:
                break
                
    else:
        try:
            # random_user_agent = random.choice(user_agents)
            options = uc.ChromeOptions()
            options.add_argument("--excludeSwitches=enable-automation")
            options.add_argument("--excludeSwitches=enable-logging")
            options.add_argument('--lang=en-US')
            # options.add_argument(f"--user-agent={user_agent}")
            # options.add_argument(f'--proxy-server={proxy_ip}')
            # options.add_argument(f'--proxy-server=http://{proxy_host}:{proxy_port}')
            # options.add_argument(f'--proxy-auth={proxy_username}:{proxy_password}')
            options.add_argument("ignore-certificate-errors")
            options.add_argument('--headless')
            driver = uc.Chrome(options=options,version_main = 114)
            driver.set_page_load_timeout(60)
        except:
            sys.stderr = open('error.log', 'a+',encoding='utf-8')
            traceback.print_exc()
            sys.stderr.close()

        try:
            driver.get('https://visa.vfsglobal.com/gbr/en/ita/login')
            time.sleep(20)
        except:
            pass
        

        # cookies reject button click
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"onetrust-reject-all-handler"))).click()
            time.sleep(5)
        except:
            pass
        Flag=False
        # recaptcha solve
        try:
            click_checkbox(driver)
            time.sleep(1)
            request_audio_version(driver)
            time.sleep(1)
            Flag=solve_audio_captcha(driver)
            # driver.switch_to.default_content()
            time.sleep(10)
        except:
            pass
        try:
            driver.switch_to.default_content()
        except:
            pass
        if Flag:
            try:
                driver.close()
                time.sleep(5)
            except:
                pass
            try:
                error_message="Booking Website link: https://visa.vfsglobal.com/gbr/en/ita/book-an-appointment\n\nPlease, for this website fix the error and retry to run this program.\n"
                send_mail(error_message)
                exit()
            except:
                pass
    
    try:
        # Record the end time
        end_time = datetime.datetime.now()
        # Calculate the time difference
        time_difference = end_time - start_time
        # Check if the time difference exceeds 30 minutes
        if time_difference.total_seconds() >= 28 * 60:
            try:
                driver.close()
            except:
                pass
            exit()
    except:
        pass 

    # enter input email
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID,'mat-input-0'))).send_keys("email")
        # time.sleep(3)
    except:
        try:
            error_message="Booking Website link: https://visa.vfsglobal.com/gbr/en/ita/book-an-appointment\n\nPlease, for this website fix the error and retry to run this program.\n"
            send_mail(error_message)
            exit()
        except:
            pass
        pass
    # enter input password
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID,'mat-input-1'))).send_keys("password")
        # time.sleep(3)
    except:
        pass

    # sigin in button click
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/div/app-login/section/div/div/mat-card/form/button"))).click()
        time.sleep(20)
    except:
        pass
    
    # Booking button click
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/div/app-dashboard/section[1]/div/div[2]/button"))).click()
        time.sleep(15)
    except:
        pass

    # Choose your Visa Application Centre
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,"mat-select-value-1"))).click()
        time.sleep(3)
    except:
        pass
    # select 
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,"mat-option-1"))).click()
        time.sleep(15)
    except:
        pass

    # Choose your appointment category
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,"mat-select-value-3"))).click()
        time.sleep(3)
    except:
        pass
    # select
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,"mat-option-3"))).click()
        time.sleep(30)
    except:
        pass
    
    try:
        soup=bs(driver.page_source,'html.parser')
        text_value=soup.find('div',attrs={'class':'alert alert-info border-0 rounded-0'}).text.strip()
    except:
        text_value=''
    if text_value.find("Earliest Available Slot")!=-1:
        send_message="In Italy, Appointment is available now!\n\nBooking Website link: https://visa.vfsglobal.com/gbr/en/ita/book-an-appointment\n"
        send_mail(send_message)
        # print("In Italy, Appointment is available now!")
    else:
        send_message="In Italy there are no appointment available now!\n\nBooking Website link: https://visa.vfsglobal.com/gbr/en/ita/book-an-appointment\n"
        send_mail(send_message)
        # print("In Italy there are no appointment available now!")
    try:
        driver.close()
    except:
        pass

    






# main function

if __name__=="__main__":
    try:
        automation_function()
    except:
        sys.stderr = open('error.log', 'a+',encoding='utf-8')
        traceback.print_exc()
        sys.stderr.close()
        pass
    





