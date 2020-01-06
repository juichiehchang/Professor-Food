# import pygame
# import os, glob

# class pygame_layout():
#     def __init__(self, window_width = 1200, window_height = 600, 
#                 img_width = 150, img_height = 150):
#         self.window_width = window_width
#         self.window_height = window_height
#         self.img_width = img_width
#         self.img_height = img_height

#     def set_img(self, img = 'default.jpg', x, y):
#         gameDisplay.blit(img, (x, y))


#     def display(self, path = './res_img/'):
        
#         pygame.init()
#         gameDisplay = pygame.display.set_mode((self.window_width, self.window_height))
#         pygame.display.set_caption('A bit Racey')

#         black = (0,0,0)
#         white = (255,255,255)

#         clock = pygame.time.Clock()
#         crashed = False

#         img_list = sorted(glob.glob(path+'*.jpg'), key = os.path.getmtime)

#         for i in range(img_list):


    
#     def 





import matplotlib.pyplot as plt
import numpy as np
import os, glob

from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
from time import sleep

myfont = FontProperties(fname='/System/Library/Fonts/PingFang.ttc',size=13)

list_title = [1,2,3,4,5,6]
myfont = FontProperties(fname='/System/Library/Fonts/PingFang.ttc',size=13)
path = './res_img/'
img_list = sorted(glob.glob(path+'*.jpg'), key = os.path.getmtime)
print(img_list)

n = len(list_title)
if n%2 is 0:
    window_x = int(n/2)
else:
    window_x = int(n/2)+1

plt.figure(num = 'restaurant', figsize = (20, 7))
for i in range(min(len(list_title), len(img_list))):
    ax = plt.subplot(2, window_x, i+1)

    if img_list[i] != "":
        photo = plt.imread(img_list[i])
    else:
        photo = plt.imread('default.jpg')

    ax.imshow(photo)
    plt.axis('off')
    plt.title(list_title[i], fontproperties=myfont)

plt.show(block=False)
plt.pause(3)
plt.close('all')

plt.figure(num = '123', figsize = (20, 7))
for i in range(min(len(list_title), len(img_list))):
    ax = plt.subplot(2, window_x, i+1)

    if img_list[i] != "":
        photo = plt.imread(img_list[i])
    else:
        photo = plt.imread('default.jpg')

    ax.imshow(photo)
    plt.axis('off')
    plt.title(list_title[i], fontproperties=myfont)

plt.show(block=False)
plt.pause(3)
plt.close('all')
print(1223)
sleep(4)
print(1222)


