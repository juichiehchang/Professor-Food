# import requests

# url = 'http://172.20.10.6:3000/target'
# myobj = {'target': '1'} # send 1 is a request that ask robot to come; 
# #						# send 2 request to take the food

# x = requests.post(url, data = myobj)

# print(x.text)



import matplotlib.pyplot as plt
import numpy as np
import os, glob

from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# myfont = FontProperties(fname='/System/Library/Fonts/PingFang.ttc',size=13)

# list_title = []
# myfont = FontProperties(fname='/System/Library/Fonts/PingFang.ttc',size=13)
# path = './res_img/'
# img_list = sorted(glob.glob(path+'*.jpg'), key = os.path.getmtime)
# print(img_list)

# n = len(list_title)
# if n%2 is 0:
#     window_x = int(n/2)
# else:
#     window_x = int(n/2)+1

# plt.figure(num = 'restaurant', figsize = (20, 9))
# for i in range(min(len(list_title), len(img_list))):
#     ax = plt.subplot(2, window_x, i+1)

#     if img_list[i] != "":
#         photo = plt.imread(img_list[i])
#     else:
#         photo = plt.imread('default.jpg')

#     ax.imshow(photo)
#     plt.axis('off')
#     plt.title(list_title[i].text, fontproperties=myfont)

# plt.show(block=False)
# plt.pause(5)
# plt.close('all')

# get the total sentence

import pyaudio
import wave
import speech_recognition as sr
import datetime
from collections import deque
import math
import audioop
import os
from chinese import ChineseAnalyzer


foo = '我想要吃巧克力'
wants = ["一杯", "一個", "想要吃", "想要喝", "想要", "想吃", "想喝", "要", "吃"]

def textParsing( text):

	analyzer = ChineseAnalyzer()
	result = analyzer.parse(text, traditional = True)
	return result.tokens()

def split_(text):
	final = ""
	for want in wants:
		food = text.split(want)
		print(food)
		if len(food) != 1:
			final = food[len(food)-1]
			break
		else:
			final = text
	return final

# parsing the sentence
parsing = textParsing(foo)

food_text = False
finding_dish = False
food_send2panda = ""
# split 
for i in wants:
	for j in parsing:
		if food_text:
			food_send2panda += j
		if i == j:
			food_text = True

	if food_text:
		break

	if food_send2panda == "":
		food_send2panda = parsing

print("food:", food_send2panda)

food_send2panda = split_(food_send2panda)
print(food_send2panda)


