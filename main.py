print("V1.0 - made by @thetwoguy on dc")
# Imports for white people
import random
import string
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time
import sys

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
user_agent = user_agent_rotator.get_random_user_agent()

webdriverOptions = webdriver.ChromeOptions()
webdriverOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
webdriverOptions.add_argument('--disable-infobars')
webdriverOptions.add_argument('--disable-popup-blocking')
# webdriverOptions.add_extension('hcaptcha.crx')
webdriverOptions.add_argument(f'--user-agent="{user_agent}"')
driver = webdriver.Chrome()

accountNumber = 1


def randomEmail(nigga_email):
    return 'samizerfaoui2'


def randomUsername(nigga_username):
    return 'ItzMeh' + str(random.randint(40, 1000))


def randomPassword(nigga_password):
    return 'Rz29#sa038173!'


driver.close()


def blackMan():
    timeout = 5
    Email = randomEmail(14) + "@gmail.com"
    Username = randomUsername(4)
    Password = randomPassword(14)
    DateOfWhite = random.choice(["07", "07"]) + "/" + random.choice(["12", "12"]) + "/" + random.choice(
        ["2005", "2005"])
    print(f"{Username} {Password}")
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(use_subprocess=True, options=options)
    driver.get("https://account.riotgames.com/")
    f = open('accountsforwhitepeople.txt', 'a')

    values = {
        "sign_in_xpath": '/html/body/div[2]/div/main/div/form/div/h5',
        "create_account_xpath": '/html/body/div[2]/div/main/div/form/div/div/div[3]/span[2]/a',
        "what_email_xpath": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[1]/h5',
        "email_textbox": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div[1]/div/input',
        "red_arrow": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/button',
        # "first_red_arrow": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/button',
        "when_born": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[1]/h5[1]',
        "dob_xpath": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div/div[1]/input',
        "choose_username": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[1]/h5[1]',
        # "second_red_arrow": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/button',
        "user_textbox": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div/div/input',
        "choose_password": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[1]/h5[1]',
        "password_xpath1": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div[1]/div/input',
        "password_xpath2": '/html/body/div[2]/div/div/div[2]/div/div[2]/form/div/div[2]/div/div[3]/div/input',
        "acc-management": '/html/body/div[2]/div[1]/div[1]/nav/div/h1'

    }

    signINCheck = EC.presence_of_element_located(
        (By.XPATH, values["sign_in_xpath"]))  # check for Sign In text
    print("check for 'Sign In' text")
    WebDriverWait(driver, timeout).until(signINCheck)
    print("found 'Sign In' text")
    print("scrolling down")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down
    print("finding create account button")
    driver.find_element(by=By.XPATH,
                        value=values["create_account_xpath"]).click()  # click Create Account
    print("clicked create account button")
    print("check for 'What's your email?' text")
    signUPCheck = EC.presence_of_element_located(
        (By.XPATH, values['what_email_xpath']))  # check for What's your email?
    WebDriverWait(driver, timeout).until(signUPCheck)
    print("found 'What's your email?' text")
    print("Typing Email Field")
    driver.find_element(by=By.XPATH,
                        value=values["email_textbox"]).send_keys(
        Email)  # fill random E-Mail
    f.write('E-mail: ' + Email + '\n')  # write e-mail to file
    print(f"Typed {Email}")
    print("scolling down")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down
    print("clicking arrow to continue")
    driver.find_element(by=By.XPATH,
                        value=values["red_arrow"]).click()  # click red arrow
    print("finding 'When were you born?' textbox")
    dobUPCheck = EC.presence_of_element_located((By.XPATH,
                                                 values["when_born"]))  # check for When were you born? text
    WebDriverWait(driver, timeout).until(dobUPCheck)
    print("found 'When were you born?' textbox")
    print("filling birthdate textbox")
    driver.find_element(by=By.XPATH,
                        value=values["dob_xpath"]).send_keys(
        DateOfWhite)  # fill random date of birth
    f.write('DOB: ' + DateOfWhite + '\n')
    print(f"date used: {DateOfWhite}")
    print("clicking red arrow")
    driver.find_element(by=By.XPATH,
                        value=values["red_arrow"]).click()  # click red arrow again
    print("clicked red arrow")
    print("check for 'Choose a username' text")
    usernameCheck = EC.presence_of_element_located((By.XPATH,
                                                    values["choose_username"]))  # check for Choose a username text
    WebDriverWait(driver, timeout).until(usernameCheck)
    print("found 'Choose a username' text")
    print("entering username")
    driver.find_element(by=By.XPATH,
                        value=values["user_textbox"]).send_keys(
        Username)
    f.write('Username: ' + Username + '\n')
    print(f"entered {Username}")
    print("clicking red arrow")
    driver.find_element(by=By.XPATH,
                        value=values["red_arrow"]).click()  # click red arrow again
    print("clicked red arrow")
    print("checking for 'Choose a password' text")
    passwordCheck = EC.presence_of_element_located((By.XPATH,
                                                    values["choose_password"]))  # check for Choose a password text
    WebDriverWait(driver, timeout).until(passwordCheck)
    print("entering password")
    driver.find_element(by=By.XPATH,
                        value=values["password_xpath1"]).send_keys(
        Password)
    driver.find_element(by=By.XPATH,
                        value=values["password_xpath2"]).send_keys(
        Password)
    print("entered password, writing file")
    f.write('Password: ' + Password + '\n')
    f.write('/////////////////////////////////' + '\n')
    f.close()
    print("done writing in file")
    print("finishing up")
    driver.find_element(by=By.XPATH,
                        value=values["red_arrow"]).click()  # click red arrow again
    print("clicked confirm red arrow")
    print("waiting for acc management tab")
    doneCheck = EC.presence_of_element_located(
        (By.XPATH, values["acc-management"]))  # check for When were you born? text
    try:
        WebDriverWait(driver, 100).until(doneCheck)
        print("found, done")
    except TimeoutException:
        print("TimeoutException occurred, either a captcha popped up or your internet is shit mf")
        driver.close()


blackMan()
print("Thx for using the gen! you may exit or restart the program")
while True:
    blackMan()
