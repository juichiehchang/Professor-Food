from time import sleep
#from webcrawler.cookie import load_cookie
from .cookie import load_cookie
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import getch
import re

import shutil
import requests
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
import glob, os
import copy


def keyboard(driver):
    while True:
        pressedKey = getch.getch()
        if pressedKey == 'u':
            scroll_up(driver)
        elif pressedKey == 'd':
            scroll_down(driver)
        elif pressedKey == 'z':
            return
        
# Startup the driver
def startup():
    # Using Chrome to access web
    #driver = webdriver.Chrome()
    
    chromeOptions = Options()
    # Open the browser in full screen
    chromeOptions.add_argument("--window-size=1920,1080")
    # Don't show automation mode
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromeOptions.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(chrome_options=chromeOptions)

    # Get the website
    driver.get('https://www.foodpanda.com.tw/')

    return driver

# Load cookie and refresh the website
def refresh_cookie(driver, path_to_cookie):
    load_cookie(driver, path_to_cookie)
    driver.refresh()
    sleep(2)

# Scroll down
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, window.scrollY + 400);")

# Scroll up
def scroll_up(driver):
    driver.execute_script("window.scrollTo(0, 0);")

# Set current location 
def set_location(driver, location, delivery=True):
    location_box = driver.find_element_by_id('delivery-information-postal-index')
    location_box.send_keys(location)
    sleep(3)

    avoid_location(driver)

    if delivery:
        driver.find_element_by_xpath('//button[text()="外送"]').click()
    else:
        driver.find_element_by_xpath('//button[text()="外帶自取"]').click()
    sleep(3)

# Search for food
def search_food(driver, food):
    check_ad(driver)
    # click the search icon
    driver.find_element_by_xpath('//span[@class="search-icon"]').click()
    search_box = driver.find_element_by_class_name('restaurants-search-input')
    search_box.send_keys(food)
    sleep(3)

# Strip "()"
def strip_parentheses(s):
    #a = copy.copy(s)
    #p = re.compile('\s\(.*\)')
    #return p.sub('', a, 1)
    return s.split("(")[0]

# Strip topping parentheses
def strip_top_parentheses(s):
    p = re.compile('\u3010.*\u3011')
    return p.sub('', s, 1)

# Get restaurant information
def get_restaurants(driver):
    check_ad(driver)
    #restaurants = driver.find_elements_by_xpath('//span[@class="name fn"]')
    #restaurants = [r for r in restaurants if r.text != ""]
    restaurants = []
    selected = []
    urls = []
    count = i = 0
    # Only get first 10 restaurants
    while count <= 10:
        i += 1
        #e = driver.find_element_by_xpath('(//span[@class="name fn"])[' + str(i) + ']')
        e = driver.find_element_by_xpath('(//figure[@class="vendor-tile js-vendor-tile"])['+str(i)+']')

        name_withp = e.find_element_by_xpath('.//span[@class="name fn"]').text
        name = strip_parentheses(name_withp)

        if name != "" and name not in selected:
            restaurants += [name_withp]
            selected += [name]
            restaurants_url = e.find_element_by_xpath('.//div[contains(@class, "vendor-picture")]').get_attribute('style')

            if restaurants_url != "":
                restaurants_url = restaurants_url.split('("')[1]
                restaurants_url = restaurants_url.split('"')[0]
            urls += [restaurants_url]
            count += 1

    return restaurants, urls

def get_restaurants_url(driver):

    restaurants_url = []

    lists = driver.find_elements_by_xpath('//ul[@class="vendor-list opened"]/li/div/a/figure/picture/div')

    for i in range(10):
        url = lists[i].get_attribute('style')
        restaurants_url += [url]

    for i in range(len(restaurants_url)):
        if restaurants_url[i] != "":
            restaurants_url[i] = restaurants_url[i].split('("')[1]
            restaurants_url[i] = restaurants_url[i].split('"')[0]

    return restaurants_url

def download_img(urllist, path='./res_img/'):

    for i in range(len(urllist)):
        if urllist[i] != "":
            response = requests.get(urllist[i], stream = True)
            with open(path+str(i)+'.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

        else:
            url = 'https://pbs.twimg.com/profile_images/920707349656064000/_SW1aphc_400x400.jpg'
            response = requests.get(url, stream = True)
            with open(path+str(i)+'.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

    return 

def show_img(list_title, path):

    myfont = FontProperties(fname='/System/Library/Fonts/PingFang.ttc',size=13)

    img_list = sorted(glob.glob(path+'*.jpg'), key = os.path.getmtime)
    print(img_list)
    
    n = len(list_title)
    if n%2 is 0:
        window_x = int(n/2)
    else:
        window_x = int(n/2)+1
    
    plt.figure(num = 'restaurant', figsize = (20, 9))
    for i in range(min(len(list_title), len(img_list))):
        ax = plt.subplot(2, window_x, i+1)

        if img_list[i] != "":
            photo = plt.imread(img_list[i])
        else:
            photo = plt.imread('default.jpg')

        ax.imshow(photo)
        plt.axis('off')
        plt.title(strip_parentheses(list_title[i].text), fontproperties=myfont)

    plt.show(block=False)
    plt.pause(3)
    plt.close('all')

    # Delete image in folder
    files = glob.glob(path+'*')
    for f in files:
        os.remove(f)

    
    return


# Select restaurant with the given name
def select_restaurant(driver, res_name):
    check_ad(driver)

    #try:
    #    r = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="name fn" and text()="' + res_name + '"]/parent::span/parent::figcaption/parent::figure/parent::a')))
    #    r.click()
    #except TimeoutException:
    #    print("Wait too long, not clickable")
    r = driver.find_element_by_xpath('//span[@class="name fn" and text()="' + res_name + '"]/parent::span/parent::figcaption/parent::figure/parent::a')
    href = r.get_attribute('href')
    driver.execute_script("window.open('" + href + "');")
    driver.switch_to.window(driver.window_handles[1])

    sleep(3)

# Get dish lists
def get_dish_lists(driver):
    # Find dish category title
    headers = driver.find_elements_by_xpath('//h2[@class="dish-category-title"]')
    # Find dish lists
    lists = driver.find_elements_by_xpath('//ul[@class="dish-list"]')

    dish_lists = {}
    for i in range(0, len(headers)):
        # Ignore "注意事項"
        if headers[i].text == "※注意事項":
            continue
        dishes = lists[i].find_elements_by_xpath('.//h3[@class="dish-name fn p-name"]')
        dish_lists[headers[i].text] = [d for d in dishes if d.text != ""]
    return dish_lists

def get_dish_url(driver):

    dish_url = []

    lists = driver.find_elements_by_xpath('//ul[@class="dish-list"]/li/div/div/picture/div')

    for i in range(len(lists)):
        url = lists[i].get_attribute('style')
        dish_url += [url]

    for i in range(len(dish_url)):
        if dish_url[i] != "":
            dish_url[i] = dish_url[i].split('("')[1]
            dish_url[i] = dish_url[i].split('"')[0]

    return dish_url


# Select dish
def select_dish(driver, dish_name):
    scroll_up(driver)
    driver.find_element_by_xpath('//span[text()="' + dish_name + '"]').click()
    sleep(2)
    
# Check if ad is presented
def check_ad(driver):
    try:
        ad = driver.find_element_by_class_name('ab-center-cropped-img')
        ad.click()
        sleep(1)
    except NoSuchElementException:
        pass

# Avoid search location
def avoid_location(driver):
    try:
        ex = driver.find_element_by_xpath('.//span[@class="map-close"]')
        ex.click()
        sleep(1)
    except NoSuchElementException:
        pass

# Check if there is any topping lists
def check_topping_lists(driver):
    # Check if there is any topping lists
    try:
        driver.find_element_by_xpath('//div[@class="product-add-to-cart"]')
    except NoSuchElementException:
        return False
    return True

# Get topping_lists
def get_topping_lists(driver, selected):
    # Click show-more buttons
    try:
        more = driver.find_elements_by_xpath('//span[@class="product-toppings-more-chevron"]/parent::a')
        for m in more:
            m.click()
        sleep(2)
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass
    
    # Find topping list titles
    #titles = driver.find_elements_by_xpath('//div[@class="product-topping-list"]')

    sleep(3)
    # Only parse must-pick toppings

    titles = driver.find_elements_by_xpath('.//div[contains(@class, "required-list")]')
    for t in titles:
        title = t.find_element_by_xpath('.//span[@class="product-topping-list-title-text"]').text
        # ignore 注意事項
        if title not in selected and title != "※注意事項":
            c_str = t.find_element_by_xpath('.//span[@class="product-topping-list-tag"]').text.split()
            if not c_str:
                return ['fake']
            count=int(t.find_element_by_xpath('.//span[@class="product-topping-list-tag"]').text.split()[0])
            choices = [e.text for e in t.find_elements_by_xpath('.//span[@class="radio-text"]')]
            selected += [title]
            return [title, count, choices]
    
    return []
        
# Select topping
def select_topping(driver, topping_name, title):
    # Space problem!!!
    #driver.find_element_by_xpath('.//span[@class="radio-text" and text()="'+ topping_name +'"]').click()
    t = driver.find_element_by_xpath('//span[@class="product-topping-list-title-text" and text()="' + title + '"]/parent::h3/parent::div')
    elements = t.find_elements_by_xpath('.//span[@class="radio-text"]')
    for e in elements:
        if topping_name in e.text:
            e.click()
            break
    sleep(1)

# Special instruction
def send_instruction(driver, message):
    i = driver.find_element_by_xpath('//textarea[@class="product-special-instructions-textarea js-topping-special-instructions js-input-in-modal"]')
    i.send_keys(message)
    sleep(3)

# Confirm purchase
def confirm_purchase(driver):
    driver.find_element_by_xpath('//button[@class="product-add-to-cart-button js-toppings-add-to-cart button full"]').click()
    sleep(3)

# Checkout
def checkout(driver):
    driver.find_element_by_xpath('.//button[@class="button full btn-checkout btn-to-checkout"]').click()
    sleep(2)

# Finish and pay
def finish_and_pay(driver):
    target = driver.find_element_by_xpath('.//button[@class="button checkout__payment__finish-and-pay-submit-button js-ripple"]')
    ActionChains(driver).move_to_element(target).click_and_hold().perform()
    sleep(1)
    ActionChains(driver).release().perform()
    sleep(2)
