# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    : python 3 , 答题闯关辅助，截屏 ，OCR 识别，百度搜索

import io
import urllib.parse
import webbrowser
import requests
import base64
import matplotlib.pyplot as plt
from threading import Thread
from PIL import Image
import os
from aip import AipOcr
import methods
import re
from selenium import webdriver
import urllib

def pull_screenshot(png_name):
    os.system("adb shell screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png %s" % png_name)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
            
# 百度OCR API  ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
APP_ID = "10721147"
API_KEY = "kLO2M8CrMAAqy3X2nxnTmiFG"
SECRET_KEY = "BNsas1Yyj460jkigPRFbt4gpWBAuOMZK"

client = AipOcr (APP_ID , API_KEY , SECRET_KEY)

re_no = re.compile ("^[\d]+[\.]*")
date = "1月25日"
browser = webdriver.Firefox()
question_num = 1

while True:
    try:
        print ("\n\n\n\n")
        para = input ("Press anykey to start:")
        if para == "exit":
            break
        
        png_name = r"./screenshot%d.png" % question_num
        question_num += 1
        pull_screenshot(png_name)
        img = Image.open(png_name)

        # 切割图片-问题
        #region = img.crop((0 , 700 , 1440 , 1180))
        region = img.crop((0 , 400 , 1440 , 1560))
        imgByteArr = io.BytesIO()
        region.save(imgByteArr, format="PNG")
        image_data = imgByteArr.getvalue()

        result = client.basicGeneral(image_data);
        question = ""
        choices = []
        for element in range (0 , result["words_result_num"] - 3):
            question += result["words_result"][element]["words"]
        
        question = question.replace (re_no.match (question)[0] , "")
        question = question.replace ("的今天" , date)
        
        browser.get('https://www.baidu.com/s?wd=' + question)
        
        
        for element in range (result["words_result_num"] - 3 , result ["words_result_num"]):
            choices.append (result["words_result"][element]["words"])
        # #切割图片-答案
        # region = img.crop((0 , 860 , 1440 , 1560))
        # region.show()
        # imgByteArr = io.BytesIO()
        # region.save(imgByteArr, format="PNG")
        # image_data = imgByteArr.getvalue()

        # result = client.basicGeneral(image_data);
        # choices = []
        
        # for element in result["words_result"]:
            # choices.append (element["words"])

        # js = " window.open('http://www.acfun.cn/')" #可以看到是打开新的标签页 不是窗口
        # browser.execute_script(js)
        # browser.close()
        print (choices)
        if len (choices) != 0:
            # 多线程
            m2 = Thread(methods.run_algorithm(1, question, choices))
            m3 = Thread(methods.run_algorithm(2, question, choices))
            m2.start()
            m3.start()
        file = open (r".\test.txt" , "a" , encoding = "utf-8")  
        file.write (question)
        file.write ("\n")
        for i in choices:
            file.write (i)
            file.write ("\n")
        file.close()

    except:
        print ("Error")
