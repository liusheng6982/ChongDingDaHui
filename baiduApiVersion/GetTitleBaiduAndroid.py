# -*- Python 3.6.0 -*-
# -*- coding: utf-8 -*-

# @Author : ud63isyl
# @Time : 2018/1/25 20:23
# @desc : 答题闯关辅助，截屏 ，OCR 识别，百度搜索

import io
import urllib.parse
import webbrowser
import requests
import base64
import matplotlib.pyplot as plt
from PIL import Image
import os
from baidu_ocr import baidu_ocr

def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png .')

def config():
    baidu_para = open (r".\baidu-key.txt" , "r" , encoding = "utf-8")
    temp = baidu_para.read()
    para_list = temp.split ("\n")
    APP_ID = para_list[0].split(":")[-1]
    API_KEY = para_list[1].split(":")[-1]
    SECRET_KEY = para_list[2].split(":")[-1]
    
ocr_client = baidu_ocr()
img = Image.open("./screenshot.png")
region = img.crop((0 , 400 , 1440 , 1560))
imgByteArr = io.BytesIO()
region.save(imgByteArr, format="PNG")
image_data = imgByteArr.getvalue()

result = ocr_client.img_to_str (image_data)
print (result)
'''   
pull_screenshot()
img = Image.open("./screenshot.png")

# 用 matplot 查看测试分辨率，切割

region = img.crop((50, 350, 1000, 560)) # 坚果 pro1
#region = img.crop((75, 315, 1167, 789)) # iPhone 7P

#im = plt.imshow(img, animated=True)
#im2 = plt.imshow(region, animated=True)
#plt.show()

# 百度OCR API  ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
api_key = ''
api_secret = ''


# 获取token
host =  'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+api_secret
headers = {
    'Content-Type':'application/json;charset=UTF-8'
}

res = requests.get(url=host,headers=headers).json()
token = res['access_token']


imgByteArr = io.BytesIO()
region.save(imgByteArr, format='PNG')
image_data = imgByteArr.getvalue()
base64_data = base64.b64encode(image_data)
r = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
              params={'access_token': token}, data={'image': base64_data})
result = ''
for i in r.json()['words_result']:
    result += i['words']
result = urllib.parse.quote(result)
webbrowser.open('https://baidu.com/s?wd='+result)
'''