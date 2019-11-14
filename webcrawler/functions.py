from time import sleep
from cookies import load_cookie
from selenium.common.exceptions import NoSuchElementException

# Load cookie and refresh the website
def refresh_cookie(driver, path_to_cookie):
    load_cookie(driver, path_to_cookie)
    driver.refresh()
    sleep(2)
    
# Set current location 
def set_location(driver, location, delivery=True):
    location_box = driver.find_element_by_id('delivery-information-postal-index')
    location_box.send_keys(location)
    sleep(5)

    avoid_location(driver)

    if delivery:
        driver.find_element_by_xpath('//button[text()="外送"]').click()
    else:
        driver.find_element_by_xpath('//button[text()="外帶自取"]').click()
    sleep(5)

# Search for food
def search_food(driver, food):
    check_ad(driver)
    # click the search icon
    driver.find_element_by_xpath('//span[@class="search-icon"]').click()
    search_box = driver.find_element_by_class_name('restaurants-search-input')
    search_box.send_keys(food)
    sleep(5)

# Get restaurant information
def get_restaurants(driver):
    check_ad(driver)
    restaurants = driver.find_elements_by_xpath('//span[@class="name fn"]')
    restaurants = [r for r in restaurants if r.text != ""]
    return restaurants

# Select restaurant with the given name
def select_restaurant(driver, res_name):
    check_ad(driver)
    driver.find_element_by_xpath('//span[@class="name fn" and text()="' + res_name + '"]').click()
    sleep(5)

# Get dish lists
def get_dish_lists(driver):
    # Find dish category title
    headers = driver.find_elements_by_xpath('//h2[@class="dish-category-title"]')
    # Find dish lists
    lists = driver.find_elements_by_xpath('//ul[@class="dish-list"]')

    dish_lists = {}
    for i in range(0, len(headers)):
        dishes = lists[i].find_elements_by_xpath('.//h3[@class="dish-name fn p-name"]')
        dish_lists[headers[i].text] = [d for d in dishes if d.text != ""]
    return dish_lists

# Select dish
def select_dish(driver, dish_name):
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

# Get topping_lists
def get_topping_lists(driver):
    # Check if there is any topping lists
    try:
        driver.find_element_by_xpath('//div[@class="modal-body"]')
        sleep(1)
    except NoSuchElementException:
        return None

    # Click show-more buttons
    try:
        more = driver.find_elements_by_xpath('//span[@class="product-toppings-more-chevron"]')
        for m in more:
            m.click()
        sleep(2)
    except NoSuchElementException:
        pass
    
    # Find topping list titles
    #titles = driver.find_elements_by_xpath('//div[@class="product-topping-list"]')

    topping_lists = {}
    # Only parse must-pick toppings
    titles = driver.find_elements_by_xpath('.//div[@class="product-topping-list required-list"]')
    for t in titles:
        title = t.find_element_by_xpath('.//span[@class="product-topping-list-title-text"]').text
        count=int(t.find_element_by_xpath('.//span[@class="product-topping-list-tag"]').text.split()[0])
        choices = [e.text for e in t.find_elements_by_xpath('.//span[@class="radio-text"]')]
        topping_lists[title] = [count, choices]
    
    return topping_lists
        
# Select topping
def select_topping(driver, topping_name):
    # Space problem!!!
    #driver.find_element_by_xpath('.//span[@class="radio-text" and text()="'+ topping_name +'"]').click()
    elements = driver.find_elements_by_xpath('//span[@class="radio-text"]')
    for e in elements:
        if topping_name in e.text:
            e.click()
            break
    sleep(1)

# Confirm purchase
def confirm_purchase(driver):
    driver.find_element_by_xpath('//button[@class="product-add-to-cart-button js-toppings-add-to-cart button full"]').click()
    sleep(5)

# Checkout
def checkout(driver):
    driver.find_element_by_xpath('.//button[@class="button full btn-checkout btn-to-checkout"]').click()
    sleep(2)

# Finish and pay
def finish_and_pay(driver):
    driver.find_element_by_xpath('.//button[@class="button checkout__payment__finish-and-pay-submit-button js-ripple]').click()
    sleep(2)
