from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import undetected_chromedriver as uc


# Create a WebDriver with the proxy settings
chrome_options = uc.ChromeOptions()
driver = webdriver.Chrome()

# Navigate to the website
driver.get('https://account.riotgames.com/')

# Wait for some time to see the result (you can use WebDriverWait for more precise control)
input()
# Close the browser when done
driver.quit()
