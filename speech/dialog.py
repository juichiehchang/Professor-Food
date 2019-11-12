from speechRecognizer import listener
from speaker import speaker
import time

###define###

LISTEN_FOOD = 1
LISTEN_REPLY = 2
FOOD_REPLY = 3
ASK_DETIALED = 4
ASK_SOMETHING_ELSE = 5



STATE = LISTEN_FOOD
is_dialog = True

listen = listener()
say = speaker()
food = ""

while(is_dialog):
    print("STATE is {}".format(STATE))
    
    if STATE is LISTEN_FOOD:
        food = listen.find_food_to_foodpanda()
        print(food)
        STATE = FOOD_REPLY

    if STATE is LISTEN_REPLY:
        reply = listen.get_reply()
        print(reply)
        STATE = ASK_DETIALED

    if STATE is FOOD_REPLY:
        sentence = '好的，在麩潘打上搜尋'+food
        say.speak(sentence)
        STATE = LISTEN_REPLY

    if STATE is ASK_DETIALED:
        sentence = '妳好，請問要紅茶還是綠茶'
        say.speak(sentence)
        STATE = LISTEN_REPLY

    if STATE is ASK_SOMETHING_ELSE:
        sentence = '請問還需要些什麼嗎'





    

