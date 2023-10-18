import random
from discord_webhook import DiscordWebhook, DiscordEmbed
import undetected_chromedriver as uc
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import shutil
import aiohttp, json, requests
from fastapi import FastAPI
import os, sys
import asyncio
from riot_auth import RiotAuth, auth_exceptions

cw = shutil.get_terminal_size().columns
Version = "V1.1"
print(f"{Version} - made by @thetwoguy on dc")

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
user_agent = user_agent_rotator.get_random_user_agent()

webdriverOptions = uc.ChromeOptions()
webdriverOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
webdriverOptions.add_argument('--disable-infobars')
webdriverOptions.add_argument('--disable-popup-blocking')
# webdriverOptions.add_extension('hcaptcha.crx')
webdriverOptions.add_argument(f'--user-agent="{user_agent}"')
driver = webdriver.Chrome()

accountNumber = 1
Username = None
Password = None

driver.close()

raw_webhook = "WEBHOOKHERE"
webhook = DiscordWebhook(
    url=raw_webhook)


async def Auth(raw_webhook, Username, Password):
    embed = DiscordEmbed(title=f"Valorant Acc Checker `{Version}`", description="Account Checker INITIALIZING",
                         color="a89700")
    embed.add_embed_field(name=f"`{Username}`", value="Skins: N/A")
    webhook.add_embed(embed)
    response = webhook.execute()
    build = requests.get('https://valorant-api.com/v1/version').json()['data']['riotClientBuild']
    print('Valorant Build ' + build)

    RiotAuth.RIOT_CLIENT_USER_AGENT = build + '%s (Windows;10;;Professional, x64)'

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    CREDS = Username, Password

    auth = RiotAuth()
    try:
        await auth.authorize(*CREDS)
        embed = DiscordEmbed(title=f"Valorant Acc Gen `{Version}`", description="Account generator INITIALIZED",
                             color="056ded")
        embed.add_embed_field(name="Status", value=f"Checking: `{Username}`")
        webhook.add_embed(embed)
        response = webhook.execute()

    except auth_exceptions.RiotAuthenticationError:
        embed = DiscordEmbed(title=f"Valorant Acc Checker `{Version}`", description="Account Checker INITIALIZING",
                             color="a89700")
        embed.add_embed_field(name=f" {Username} Error: Auth Failed, Please check credentials and try again.",
                              value="N/A")
        webhook.add_embed(embed)
        response = webhook.execute()
        exit('Error: Auth Failed, Please check credentials and try again.')

    except auth_exceptions.RiotMultifactorError:
        embed = DiscordEmbed(title=f"Valorant Acc Checker `{Version}`", description="Account Checker INITIALIZING",
                             color="a89700")
        embed.add_embed_field(
            name=f" `{Username}` Accounts with MultiFactor enabled are not supported at this time.",
            value="N/A")
        webhook.add_embed(embed)
        response = webhook.execute()
        exit('Accounts with MultiFactor enabled are not supported at this time.')

    return auth

async def store(raw_webhook, Username, Password):
    auth = await Auth(raw_webhook, Username, Password)

    region = 'eu'

    token_type = auth.token_type
    access_token = auth.access_token
    entitlements_token = auth.entitlements_token
    user_id = auth.user_id

    conn = aiohttp.TCPConnector()
    session = aiohttp.ClientSession(connector=conn)

    headers = {
        'X-Riot-Entitlements-JWT': entitlements_token,
        'Authorization': 'Bearer ' + access_token,
    }

    async with session.get('https://pd.' + region + '.a.pvp.net/store/v1/offers/', headers=headers) as r:
        pricedata = await r.json()

    async with session.get('https://pd.' + region + '.a.pvp.net/store/v2/storefront/' + user_id,
                           headers=headers) as r:
        data = json.loads(await r.text())
    allstore = data.get('SkinsPanelLayout')
    singleitems = allstore["SingleItemOffers"]
    skin1uuid = singleitems[0]
    skin2uuid = singleitems[1]
    skin3uuid = singleitems[2]
    skin4uuid = singleitems[3]

    async with session.get('https://valorant-api.com/v1/weapons/skinlevels/' + skin1uuid) as r:
        skin1 = json.loads(await r.text())['data']['displayName']

    async with session.get('https://valorant-api.com/v1/weapons/skinlevels/' + skin2uuid) as r:
        skin2 = json.loads(await r.text())['data']['displayName']

    async with session.get('https://valorant-api.com/v1/weapons/skinlevels/' + skin3uuid) as r:
        skin3 = json.loads(await r.text())['data']['displayName']

    async with session.get('https://valorant-api.com/v1/weapons/skinlevels/' + skin4uuid) as r:
        skin4 = json.loads(await r.text())['data']['displayName']

    def getprice(uuid):
        for item in pricedata['Offers']:
            if item["OfferID"] == uuid:
                return item['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']

    def nightmarket(datad):
        out = []
        try:
            for item in datad["BonusStore"]["BonusStoreOffers"]:
                r = requests.get(
                    f'https://valorant-api.com/v1/weapons/skinlevels/' + item['Offer']['Rewards'][0]['ItemID'])
                skin = r.json()
                data = {
                    'name': skin['data']['displayName'],
                    'uuid': item['Offer']['OfferID'],
                    'price': {
                        'oringinal': item['Offer']['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741'],
                        'discount': item['DiscountPercent'],
                        'final': item['DiscountCosts']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741'],
                    }
                }
                out.append(data)
            return out
        except KeyError:
            return None

    ms_text = """
    Store:""".center(cw)
    print(ms_text)
    print(f"""
  {skin1} for {getprice(skin1uuid)}
  {skin2} for {getprice(skin2uuid)}
  {skin3} for {getprice(skin3uuid)}
  {skin4} for {getprice(skin4uuid)}
  """)
    embed = DiscordEmbed(title=f"Valorant Acc Gen {Version}", description="Account CHECKER FINISHED",
                         color="44c200")
    embed.add_embed_field(name="Status", value=f"SUCCESSFULLY CHECKED: `{Username}`")
    embed.add_embed_field(name="Main Shop", value=f"""
      `{skin1} for {getprice(skin1uuid)}`
      `{skin2} for {getprice(skin2uuid)}`
      `{skin3} for {getprice(skin3uuid)}`
      `{skin4} for {getprice(skin4uuid)}`
    """)
    nm = nightmarket(data)
    if nm != None:
        nm_text = """
      Night Market                                                                                  
    """.center(cw)
        print(nm_text)
        nm_items = []

        for item in nm:
            nmitem_text = f"`{item['name']}` for `{item['price']['final']}` \n Original Price: {item['price']['oringinal']}\n Discount: `{item['price']['discount']}%`\n"
            nm_items.append(nmitem_text)

        embed.add_embed_field(name="Nightmarket", value=''.join(nm_items))
        print(''.join(nm_items))
    webhook.add_embed(embed)

    response = webhook.execute()

    await session.close()


def black_man():
    def random_email(nigga_email):
        return 'samizerfaoui2'

    def random_username(nigga_username):
        return 'ItzMeh' + str(random.randint(40, 10000))

    def random_password(nigga_password):
        return 'Rz29#sa038173!'

    embed = DiscordEmbed(title=f"Valorant Acc Gen {Version}", description="Account generator INITIALIZING",
                         color="a89700")
    embed.add_embed_field(name="Username", value="N/A")
    webhook.add_embed(embed)
    response = webhook.execute()

    timeout = 5
    Username = random_username(6)
    Password = random_password(14)
    Email = random_email(14) + "@gmail.com"
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
        "acc-management": '/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/h2'

    }

    embed = DiscordEmbed(title=f"Valorant Acc Gen {Version}", description="Account generator INITIALIZED",
                         color="056ded")
    embed.add_embed_field(name="Status", value=f"generating: `{Username}`")
    webhook.add_embed(embed)
    response = webhook.execute()

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
        embed = DiscordEmbed(title=f"Valorant Acc Gen {Version}", description="Account generator FINISHED",
                             color="44c200")
        embed.add_embed_field(name="Status", value=f"SUCCESSFULLY GENERATED: `{Username}`")
        webhook.add_embed(embed)
        response = webhook.execute()
        asyncio.run(store(raw_webhook, Username, Password))
        driver.close()
    except TimeoutException:
        print("TimeoutException occurred, either a captcha popped up or your internet is shit mf")
        embed = DiscordEmbed(title=f"Valorant Acc Gen {Version}", description="Account generator NEEDS MAINTENANCE",
                             color="850000")
        embed.add_embed_field(name="Status", value=f"ERROR while generating: {Username}, Probably just a captcha")
        embed.add_embed_field(name="Status",
                              value=f"awaiting manual confirmation, please check your tab <@!802973364335280148>")
        webhook.add_embed(embed)
        response = webhook.execute()

        asyncio.run(store(raw_webhook, Username, Password))
        input()


black_man()
while True:
    black_man()
