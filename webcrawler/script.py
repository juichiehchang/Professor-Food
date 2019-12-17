from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from .cookie import load_cookie
from .functions import get_topping_lists, select_topping
from .functions import startup, refresh_cookie, keyboard, scroll_down, scroll_up, set_location, search_food
from .functions import get_restaurants, select_restaurant, get_dish_lists, select_dish
from .functions import confirm_purchase, checkout
from .functions import get_restaurants_url, get_dish_url, download_img, show_img
import glob
import matplotlib.pyplot as plt


driver = startup()

# Load cookie and refresh the webpage
refresh_cookie(driver, './webcrawler/tmp/cookie')

# Set location
set_location(driver, '台灣大學')

# Search food
search_food(driver, '漢堡')

# Get result # 
restaurants = get_restaurants(driver)
for r in restaurants:
    print(r.text)

# Get restaurants image url
restaurants_url = get_restaurants_url(driver)

# Request and download image from url
download_img(restaurants_url, path = './res_img/')

# Display the image
show_img(restaurants, path = './res_img/')

#keyboard(driver)

print("\n================================================")

# Select restaurant
select_restaurant(driver, restaurants[1].text)

# Get dish lists
dish_list = []
dish_dict = get_dish_lists(driver)
for k, vs in dish_dict.items():
    print(k + ":")
    for v in vs:
        print(v.text)
        # Convert dish to list
        dish_list += [v]

# Get dish url
# dish_url = get_dish_url(driver)

# # Send request and download the image from url
# download_img(dish_url, path = './dish_img/')


# show_img(dish_list, path = './dish_img/')

# plt.pause(20)
# plt.close('all')

#keyboard(driver)

# Select dish
select_dish(driver, "雙層宿醉漢堡")

import pdb
pdb.set_trace()
       
# Get topping lists
topping_lists = get_topping_lists(driver)
for title, [count, choices] in topping_lists.items():
    print(title + ":" + "選" + str(count))
    for c in choices:
        print(c)

# Select topping
select_topping(driver, "")

# Confirm purchase
confirm_purchase(driver)

# Checkout
checkout(driver)
exit()
