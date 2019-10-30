from selenium import webdriver
from cookies import save_cookie

driver = webdriver.Chrome()
driver.get('https://www.foodpanda.com.tw/')

foo = input()

save_cookie(driver, 'tmp/cookie')
