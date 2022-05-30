from PIL import Image
from io import BytesIO
import os,requests,base64
from array import array
import os,sys,random,time
import numpy as np


import make_captcha,solve_it,tfmain



'''
url = 'http://210.35.251.243/reader/captcha.php'
for i in range(50):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save('imgs/{}.png'.format(str(i)))
'''

train_img_path1 = 'immm/'

def save_test_imgs(train_img_path):
    data_list = os.listdir(train_img_path)
    for file in data_list[::10]:
        if file != '.DS_Store':
            img = Image.open(train_img_path + file)
            img = solve_it.dele_noise(img, N=2, Z=1)
            img = solve_it.clear_lib_line(img)
            img_list = solve_it.cut_img_to_img_list(img,30,background=255)
            for k,i in enumerate(img_list):
                random_num = str(time.time())[-10:-3].replace('.',str(random.random())[2:4])
                i.save(f'test_imgs/{file[k]}-{random_num}.png')
        os.remove(train_img_path + file)

def save_train_imgs(train_img_path):
    data_list = os.listdir(train_img_path)
    for file in data_list:
        if file != '.DS_Store':
            img = Image.open(train_img_path + file)
            img = solve_it.dele_noise(img, N=2, Z=1)
            img = solve_it.clear_lib_line(img)
            img_list = solve_it.cut_img_to_img_list(img,30,background=255)
            for k,i in enumerate(img_list):
                random_num = str(time.time())[-10:-3].replace('.',str(random.random())[2:4])
                i.save(f'train_imgs/{file[k]}-{random_num}.png')

def remove_file(train_img_path):
    data_list = os.listdir(train_img_path)
    for file in data_list:
        os.remove(train_img_path + file)


save_test_imgs(train_img_path1)
save_train_imgs(train_img_path1)
remove_file(train_img_path1)

