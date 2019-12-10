from selenium import webdriver
from cookie import save_cookie

driver = webdriver.Chrome()
driver.get('https://www.foodpanda.com.tw/')

foo = input()

save_cookie(driver, 'tmp/cookie')
