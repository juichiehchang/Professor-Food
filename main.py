from speech.speaker import speaker
from speech.speechRecognizer import listener
import time

from selenium import webdriver
from time import sleep
from webcrawler.cookie import load_cookie
from webcrawler.functions import startup, refresh_cookie, set_location, search_food
from webcrawler.functions import get_restaurants, select_restaurant, get_dish_lists, select_dish
from webcrawler.functions import get_topping_lists, select_topping
from webcrawler.functions import confirm_purchase, checkout
from webcrawler.functions import strip_top_parentheses
from webcrawler.functions import get_restaurants_url, download_img
from chinese import ChineseAnalyzer
import pinyin
from function import similar
import pygame
from pygame import mixer
import glob



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



while(is_dialog):

    if STATE is WAITING:

        # maybe wait for the bot navigation
        # after finishing navigation, state to be asking food
        STATE = ASK_WHAT_FOOD

    if STATE is ASK_WHAT_FOOD:

        # Ask what user wants
        sentence = "您好，請問想要吃點什麼呢"
        # say.speak(sentence)
        print(sentence)
        STATE = LISTEN_FOOD

    if STATE is LISTEN_FOOD:

        # In this state, find out what the food is ordered
        food = listen.find_food_to_foodpanda()
        print(food)
        STATE = FOOD_REPLY

    if STATE is FOOD_REPLY:
        sentence = '好的，在麩潘打上搜尋'+food+',請稍等'
        # say.speak(sentence)
        print(sentence)
        STATE = WEB_CRAWL

    if STATE is WEB_CRAWL:
        driver = startup()

        # Load cookie and refresh the webpage
        refresh_cookie(driver, './webcrawler/tmp/cookie')

        # set location
        set_location(driver,'台灣大學')

        #search food
        search_food(driver, food)

        # get all restaurants in website
        restaurants = get_restaurants(driver)
        restaurants_url = get_restaurants_url(driver)
        download_img(restaurants_url)

        for r in restaurants:
            print(r.text)

        print("\n================================================")

        STATE = ASK_RESTAURANTS

    if STATE is ASK_RESTAURANTS:

        # Ask which restaurant wants
        sentence = '請挑選您想要的餐廳'
        # say.speak(sentence)
        print(sentence)
        STATE = LISTEN_RESAURANTS


    if STATE is LISTEN_RESAURANTS:
        # let the user choose one restaurant and compare its string among all candidates 
        

        image = glob.glob('./res_img/*')

        pygame.init()

        display_width = 1380
        display_height = 800

        white = (255,255,255)
        black = (0,0,0)
        font = pygame.font.Font('/System/Library/Fonts/PingFang.ttc',13)

        gameDisplay = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption('A bit Racey')

        crashed = False
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

            gameDisplay.fill(white)
            #carImg = pygame.image.load('default.jpg')

            #gameDisplay.blit(carImg, (0,0))

            for i in range(9):
                x = 280 * (i%5)
                y = 100 + int(i/5) * 400
                text = font.render(restaurants[i].text, True, black, white)
                textRect = text.get_rect()
                textRect.center = (130 + (i%5) * 280, 80 + int(i/5) * 400)
                img = pygame.image.load(image[i])
                gameDisplay.blit(text, textRect)
                gameDisplay.blit(pygame.transform.scale(img,(260,200)), (x, y))

            

            pygame.display.update()
            
            choice = listen.recognize()
            print(choice)
            crashed = True

        pygame.quit()


        choice_pinyin = pinyin.get(choice, format = "numerical")
        restaurants_pinyin = [pinyin.get(r.text, format = "numerical") for r in restaurants]
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

        print("max_index:", max_index)
        select_restaurant(driver, restaurants[max_index].text)

        STATE = ASK_DISH

    if STATE is ASK_DISH:
        # ask to choose one meal
        dish_lists = get_dish_lists(driver)

        for k, vs in dish_lists.items():
            print(k + ":")
            for v in vs:
                print(v.text, end = " ")

        print("\n================================================")

        sentence = "請挑選您想吃的餐點"
        # say.speak(sentence)
        print(sentence)

        STATE = LISTEN_DISH

    if STATE is LISTEN_DISH:

        choice = listen.recognize()
        print(choice)
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

        STATE = ASK_TOPPING

    if STATE is ASK_TOPPING:

        sentence = "接下來請選擇您要的副餐"
        # say.speak(sentence)
        print(sentence)

        topping_lists = get_topping_lists(driver)

        selected = []
        while True:
                topping_list = get_topping_lists(driver, selected)
                if not topping_list:
                        break
        title, count, choices = topping_list

        print(title + ":選" + str(count))

        sentence = "在" + title + "中，選擇" + str(count) + "項"
        say.speak(sentence)
        print("\n================================================")

        similarity = 0

        for c in choices:
            print(c, end = 'numerical')

        choice = listen.recognize()
        print(choice)
        choice_pinyin = pinyin.get(choice, format = 'numerical')

        for c in choices:

            c_pinyin = pinyin.get(strip_top_parentheses(c), format = 'numerical')
            tmp = similar(c_pinyin, choice_pinyin)

            if tmp > similarity:

                similarity = tmp
                choose_topping = c

        select_topping(driver, choose_topping)

        STATE = ASK_SOMETHING_ELSE

    if STATE is ASK_SOMETHING_ELSE:

        sentence = "點餐完成，還需要什麼其他的嗎"
        # say.speak(sentence)
        print(sentence)

        reply = listen.recognize()
        print(reply)

        reply_pinyin = pinyin.get(reply, format = 'numerical')
        similarity = similar(reply_pinyin, 'bu4yong4')
    
        if similarity > 0.2:

            sentence = "好的，即將完成付款"
            # say.speak(sentence)
            print(sentence)
            confirm_purchase(driver)
            checkout(driver)
            exit()

            is_dialog = False

            

        STATE = ASK_DISH




                































        



        







