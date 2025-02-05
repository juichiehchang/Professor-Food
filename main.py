from speech.speaker import speaker
from speech.speechRecognizer import listener
import time

from selenium import webdriver
from time import sleep
from webcrawler.cookie import load_cookie
from webcrawler.functions import startup, refresh_cookie, set_location, search_food
from webcrawler.functions import get_restaurants, select_restaurant, get_dish_lists, select_dish
from webcrawler.functions import check_topping_lists, get_topping_lists, select_topping
from webcrawler.functions import confirm_purchase, checkout, finish_and_pay
from webcrawler.functions import strip_top_parentheses, strip_parentheses
from webcrawler.functions import get_restaurants_url, download_img, send_instruction
from chinese import ChineseAnalyzer
import pinyin
from function import similar
import pygame
from pygame import mixer
import glob
from showChoice import show_image, show_text, show_need



WAITING = -1
ASK_WHAT_FOOD = 1
ASK_RESTAURANTS = 2
FOOD_REPLY = 3
ASK_DISH = 4
ASK_TOPPING = 5
ASK_SOMETHING_ELSE = 6
LISTEN_FOOD = 31
LISTEN_FOOD_REPLY = 32
LISTEN_RESAURANTS = 33
LISTEN_DISH = 34


WEB_CRAWL = 80

STATE = WAITING
is_dialog = True

# use listener class to hear what users said
listen = listener()

# use speaker class to say something
say = speaker()
food = ""
restaurants = []

driver = startup()
# Load cookie and refresh the webpage
refresh_cookie(driver, './webcrawler/tmp/cookie')
# # set location
set_location(driver,'芳蘭路49號')

# Send Request
import requests
url = 'http://172.104.64.221:3000/target'
# myobj = {'target': '1'}
# x = requests.post(url, data = myobj)

# print('send request:', x)


while(is_dialog):

    if STATE is WAITING:

        # maybe wait for the bot navigation
        # after finishing navigation, state to be asking food
        STATE = ASK_WHAT_FOOD

    if STATE is ASK_WHAT_FOOD:

        # Ask what user wants
        sentence = "您好，請問想要吃點什麼呢"
        say.speak(sentence)
        #print(sentence)
        STATE = LISTEN_FOOD

    if STATE is LISTEN_FOOD:

        # In this state, find out what the food is ordered
        mixer.music.load('./hintVoice/short.mp3')
        mixer.music.play()
        food = listen.find_food_to_foodpanda()
        while not food:
            say.speak('我聽不清楚，請再講一次')
            food = listen.find_food_to_foodpanda()
        mixer.music.load('./hintVoice/short.mp3')
        mixer.music.play()
        print(food)
        
        STATE = FOOD_REPLY

    if STATE is FOOD_REPLY:
        sentence = '好的，在麩潘打上搜尋'+food+',請稍等'
        say.speak(sentence)
        print(sentence)
        STATE = WEB_CRAWL

    if STATE is WEB_CRAWL:
        

        
        

        

        #search food
        search_food(driver, food)

        # get all restaurants in website
        restaurants, restaurants_url = get_restaurants(driver)
        # print(restaurants_url)
        download_img(restaurants_url)


        restaurants_without_parenthesis = []
        
        for i in range(len(restaurants)):
            restaurants_without_parenthesis += [strip_parentheses(restaurants[i])]

        print("\n================================================")

        STATE = ASK_RESTAURANTS

    if STATE is ASK_RESTAURANTS:

        # Ask which restaurant wants

        # print(sentence)
        STATE = LISTEN_RESAURANTS


    if STATE is LISTEN_RESAURANTS:
        # let the user choose one restaurant and compare its string among all candidates 

        # Show_image function will show image with pygame and return what user said
        choice = show_image('./res_img/', False, restaurants_without_parenthesis)
        while not choice:
            say.speak('我聽不清楚，請再講一次')
            choice = show_image('./res_img/', False, restaurants_without_parenthesis)
        print(choice)
        
        choice_pinyin = pinyin.get(choice, format = "numerical")
        restaurants_pinyin = [pinyin.get(r, format = "numerical") for r in restaurants_without_parenthesis]
        similarity = 0
        index = 0
        max_index = 0

        for restaurant in restaurants_pinyin:

            tmp = similar(restaurant, choice_pinyin)


            if tmp > similarity:
                similarity = tmp
                choose_restaurant = restaurant
                max_index = index

            index += 1

        print("max_index:", restaurants[max_index])
        select_restaurant(driver, restaurants[max_index])

        STATE = ASK_DISH

    if STATE is ASK_DISH:
        # ask to choose one meal
        dish_lists = get_dish_lists(driver)
        dish = []
        for k, vs in dish_lists.items():
            print(k + ":")
            for v in vs:
                dish += [v.text]
                print(v.text, end = " ")

        print("\n================================================")

        # print(sentence)

        STATE = LISTEN_DISH

    if STATE is LISTEN_DISH:

        say.speak('請選擇您要的餐點')
        choice = show_text(False, dish)
        while not choice:
            say.speak('我聽不清楚，請再講一次')
            choice = show_text(False, dish)

        choice_pinyin = pinyin.get(choice, format = 'numerical')
        similarity = 0

        for k, vs in dish_lists.items():
            for v in vs:

                v_pinyin = pinyin.get(v.text, format = 'numerical')
                tmp = similar(v_pinyin, choice_pinyin)

                if tmp > similarity:
                    similarity = tmp
                    choose_dish = v.text

        select_dish(driver, choose_dish)

        if check_topping_lists(driver):
            STATE = ASK_TOPPING
        else:
            STATE = ASK_SOMETHING_ELSE


    if STATE is ASK_TOPPING:

        
        selected = []

        first_result = get_topping_lists(driver, [])
        # fake topping list
        if 'fake' in first_result:
            STATE = ASK_SOMETHING_ELSE
            continue
            
        # only optional topping list
        elif not first_result:
            say.speak('請說出對餐點的特別要求')
            mixer.music.load('./hintVoice/short.mp3')
            mixer.music.play()
            instruction = listen.recognize()
            send_instruction(driver, instruction)
            # 放入購物車
            confirm_purchase(driver)
            STATE = ASK_SOMETHING_ELSE
            continue
        # normal
        else:
            sentence = "接下來請選擇您要的副餐"
            say.speak(sentence)

        while True:
            topping_list = get_topping_lists(driver, selected)
            if not topping_list:
                break
            
            title, count, choices = topping_list
            if not choices:
                continue
            print(title + ":選" + str(count))

            sentence = "在" + title + "中，選擇" + str(count) + "項"
            say.speak(sentence)
            print("\n================================================")

            similarity = 0

            for c in choices:
                print(c, end = 'numerical')

            choice = show_text(False, choices)
            if not choice:
                say.speak('我聽不清楚，請再講一次')
                choice = show_text(False, choices)

            choice_pinyin = pinyin.get(choice, format = 'numerical')

            for c in choices:

                c_pinyin = pinyin.get(strip_top_parentheses(c), format = 'numerical')
                tmp = similar(c_pinyin, choice_pinyin)

                if tmp > similarity:

                    similarity = tmp
                    choose_topping = c
            print('topping chosen', choose_topping)

            select_topping(driver, choose_topping, title)

        say.speak('請說出對餐點的特別要求')
        mixer.music.load('./hintVoice/short.mp3')
        mixer.music.play()
        instruction = listen.recognize()
        send_instruction(driver, instruction)
        # 放入購物車
        confirm_purchase(driver)

        STATE = ASK_SOMETHING_ELSE

    if STATE is ASK_SOMETHING_ELSE:

        sentence = "點餐完成，還需要什麼其他的嗎"
        say.speak(sentence)

        reply = show_need(["需要","不需要"])
        while not reply:
            say.speak('我聽不清楚，請再講一次')
            reply = show_need(["需要","不需要"])

        reply_pinyin = pinyin.get(reply, format = 'numerical')
        similarity = similar(reply_pinyin, 'bu4xu1yao4')
    
        if similarity > 0.9:

            sentence = "好的，即將完成付款"
            say.speak(sentence)

            checkout(driver)
            finish_and_pay(driver)
            break

            is_dialog = False

            

        STATE = ASK_DISH

say.speak('機器人已前去取餐，請稍等')

# myobj = {'target': '2'}
# x = requests.post(url, data = myobj)
                

input()

say.speak('機器人即將送餐抵達，請準備取餐')
myobj = {'target': '1'}
x = requests.post(url, data = myobj)
                

