from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import undetected_chromedriver as uc

# Replace with your proxy URL
proxy_url = '38.154.227.167:5868'

# Configure the proxy settings
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_url
proxy.ssl_proxy = proxy_url

# Create a WebDriver with the proxy settings
chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--proxy-server=' + proxy_url)
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the website
driver.get('https://account.riotgames.com/')

# Wait for some time to see the result (you can use WebDriverWait for more precise control)
input()
# Close the browser when done
driver.quit()
