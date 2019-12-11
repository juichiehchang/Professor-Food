from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from .cookie import load_cookie
from .functions import startup, refresh_cookie, keyboard, scroll_down, scroll_up, set_location, search_food
from .functions import get_restaurants, select_restaurant, get_dish_lists, select_dish
from .functions import get_topping_lists, select_topping
from .functions import confirm_purchase, checkout

driver = startup()

# Load cookie and refresh the webpage
refresh_cookie(driver, './webcrawler/tmp/cookie')

# Set location
set_location(driver, '台灣大學')

# Search food
search_food(driver, '漢堡')

# Get result
restaurants = get_restaurants(driver)
for r in restaurants:
    print(r.text, end = " ")

#keyboard(driver)

print("\n================================================")

exit()
# Select restaurant
select_restaurant(driver, restaurants[3].text)

# Get dish lists
dish_lists = get_dish_lists(driver)
for k, vs in dish_lists.items():
    print(k + ":")
    for v in vs:
        print(v.text)

#keyboard(driver)

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
