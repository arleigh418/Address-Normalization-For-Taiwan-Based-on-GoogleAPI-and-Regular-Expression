import requests
import json
import time
from datetime import datetime
import sys
import pandas as pd

class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger("Log"+datetime.now().strftime("%Y%m%d_%H%M%S")+".txt") 

def cmp(src_data,dst_data):
    if isinstance(src_data, dict) == True:
        for key in dst_data:
            if key not in src_data:
                print("src不存在此key:"+key)
        for key in src_data:
            if key in dst_data:
                thiskey = key
                cmp(src_data[key], dst_data[key])       
            else:
                print("dst不存在此key")
    elif isinstance(src_data, list)== True:
        if len(src_data) != len(dst_data):
            print("list len: '{}' != '{}'".format(len(src_data), len(dst_data)))
        for src_list, dst_list in zip(src_data, dst_data):
            cmp(src_list, dst_list)
    else:   
        if str(src_data) != str(dst_data):
            print('存在不一致，位置如下')
            print('jSON-A --> ',src_data)
            print('jSON-B --> ',dst_data)
            print('\n'+'*'*50)
        
    

x_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=台中市大甲區文武里三民路229號sensor&language=zh-tw&key=AIzaSyCYFTENwDERhwpxuaHUeFVzKt3L0tDH5j4'
y_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=台中市大甲區大安港路173巷26號sensor&language=zh-tw&key=AIzaSyCYFTENwDERhwpxuaHUeFVzKt3L0tDH5j4'
x = requests.get(x_url)
y = requests.get(y_url)
print('jSON-A:',x_url)
print('jSON-B:',y_url)
cmp(x.json(),y.json())
print('-'*50)