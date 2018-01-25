# -*- Python 3.6 -*-
# -*- coding: utf-8 -*-

# @Author : ud63isyl
# @Time : 2018/1/9 19:34
# @desc : 百度OCR文字识别模块封装

import os , time , re
from aip import AipOcr

class baidu_ocr:
    def __init__ (self):
        if os.path.isfile (r".\baidu-key.txt"):
            baidu_para = open (r".\baidu-key.txt" , "r" , encoding = "utf-8")
            temp = baidu_para.read()
            para_list = temp.split ("\n")
            self._APP_ID = para_list[0].split(":")[-1]
            self._API_KEY = para_list[1].split(":")[-1]
            self._SECRET_KEY = para_list[2].split(":")[-1]
            
            self._client = AipOcr (self._APP_ID , self._API_KEY , self._SECRET_KEY)
            
            time_tup = time.localtime(time.time ())
            self._date = "%d月%d日" % (time_tup.tm_mon , time_tup.tm_mday)
            self._re_no = re.compile ("^[\d]+[\.]*")
        else:
            raise Exception ("缺少配置文件\"baidu-key.txt\"！")
            
    def img_to_str (self , image_data):
        result = self._client.basicGeneral(image_data);
        if result["words_result_num"] < 4:
            raise Exception ("未识别到题目！")
        question = ""
        res = []
        
        for element in range (0 , result["words_result_num"] - 3):
            question += result["words_result"][element]["words"]
        
        no_list = self._re_no.match (question)
        if no_list:
            question = question.replace (self._re_no.match (question)[0] , "")    
        
        question = question.replace ("的今天" , self._date)
        res.append (question)
        
        for element in range (result["words_result_num"] - 3 , result ["words_result_num"]):
            res.append (result["words_result"][element]["words"])

        return res
        
