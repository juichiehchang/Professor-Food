from selenium import webdriver
from time import sleep
from cookies import load_cookie
from functions import refresh_cookie, set_location, search_food
from functions import get_restaurants, select_restaurant, get_dish_lists, select_dish
from functions import get_topping_lists, select_topping
from functions import confirm_purchase, checkout
# Using Chrome to access web
driver = webdriver.Chrome()

# Get the website
driver.get('https://www.foodpanda.com.tw/')

# Load cookie and refresh the webpage
refresh_cookie(driver, 'tmp/cookie')

# Set location
set_location(driver, '台灣大學')

# Search food
search_food(driver, '漢堡')

# Get result
restaurants = get_restaurants(driver)
for r in restaurants:
    print(r.text)

print("================================================")
# Select restaurant
select_restaurant(driver, restaurants[3].text)

# Get dish lists
dish_lists = get_dish_lists(driver)
for k, vs in dish_lists.items():
    print(k + ":")
    for v in vs:
        print(v.text)

# Select dish
select_dish(driver, "藜麥元氣和牛珍珠堡組合餐")
       
# Get topping lists
topping_lists = get_topping_lists(driver)
for title, [count, choices] in topping_lists.items():
    print(title + ":" + "選" + str(count))
    for c in choices:
        print(c)

# Select topping
select_topping(driver, "玉米濃湯")

# Confirm purchase
confirm_purchase(driver)

# Checkout
checkout(driver)
exit()

# click the login button
driver.find_element_by_class_name('login-label').click()

# fill in email and password
email_box = driver.find_element_by_id('username')
email_box.send_keys('raydeadshot@gmail.com')

pass_box = driver.find_element_by_id('password')
pass_box.send_keys('Masterchief')

driver.find_element_by_xpath("//button[@type='submit']").click()
