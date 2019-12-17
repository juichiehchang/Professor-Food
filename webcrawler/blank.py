import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import os
# a =sorted(glob.glob('*.png'), key=os.path.getmtime)

a = sorted(glob.glob('./res_img/*.jpg'), key = os.path.getmtime)
b = '123'
print(type(b))






