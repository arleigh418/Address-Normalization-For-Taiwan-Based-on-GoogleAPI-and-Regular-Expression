# Author : Arleigh Chang
# date : 2019/08/04

import requests
import json
import pandas as pd
from tqdm import *
import re
import sys
from datetime import datetime

class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger("Log/Log"+datetime.now().strftime("%Y%m%d_%H%M%S")+".txt") 



def addresses_from_csv(path):  
    addresses = []
    try:
        x = pd.read_excel(path,encoding = 'utf-8')
        address = x['address'].tolist()
    except:
        x = pd.read_csv(path,encoding = 'utf-8')
        address = x['address'].tolist()
    return address


def get_api(api_key , addresses):
    print('---------------Google Api補丁開始---------------')
    transformed = []

    for query in tqdm(addresses):
        others_handle = re.compile(r'\d+樓')
        others_handle2 = re.compile(r'之+\d')
        
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+query+'&language=zh-tw&key='+api_key
        r = requests.get(url,verify = False)
        data = r.json()
        try:
            if others_handle.search(query) != None:
                if len(query)+3 - len(data['results'][0]['formatted_address']+'樓')  > 1:
                    transformed.append(data['results'][0]['formatted_address']+'樓')
                    print('地址:',query,'， 疑似異常，請檢查')
                else:
                    transformed.append(data['results'][0]['formatted_address']+'樓')

            elif others_handle2.search(query) != None:
                if  len(query)+3 - len(data['results'][0]['formatted_address']+query[query.index(others_handle.search(query).group()):]) > 1:
                    transformed.append(data['results'][0]['formatted_address']+query[query.index(others_handle.search(query).group()):])
                    print('地址:',query,'， 疑似異常，請檢查')
                else:
                    transformed.append(data['results'][0]['formatted_address']+'樓')
                

            else:
                if  len(query)+3 - len(data['results'][0]['formatted_address'])   > 1:
                    transformed.append(data['results'][0]['formatted_address'])
                    print('地址:',query,'， 疑似異常，請檢查')
                else:
                     transformed.append(data['results'][0]['formatted_address'])
               
        except:
            print('於函數get_api中異常錯誤，請檢查')
            continue
    return transformed

#儲存成Excel
def storage_excel(original_addresses , fix_addresses , final_addresses):
    try:
        print('---------------儲存檔案中--------------')
        storage = pd.DataFrame() #postcode?
        storage['original_addresses'] = original_addresses
        storage['fix_addresses'] = fix_addresses
        storage['final_addresses'] = final_addresses
        storage.to_excel('transformed_addresses.xlsx', encoding = 'big5' , index = False)
    except:
        print('於函數storage_excel中異常錯誤，請檢查')

#reference : https://www.jianshu.com/p/a5d96457c4a4 
def strQ2B(ustring): 
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288: 
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)



def num_to_ch(target_num):
    num  = ['0','1','2','3','4','5','6','7','8','9']
    ch = ['零','一','二','三','四','五','六','七','八','九']
    if len(target_num) == 1:
        final = ch[num.index(target_num)]
        return final
    elif len(target_num) == 2:
        if target_num[-1] == 0:
            final = ch[num.index(target_num[0])]+'十'
            return final

        elif target_num[0] == 1:
            final = '十' + ch[num.index(target_num[-1])]
            return final

        elif target_num[-1] !=0:
            final = ch[num.index(target_num[0])]+'十'+ch[num.index(target_num[-1])]
            return final
        
    else :
        return target_num


def ch_to_num(target_ch):
    ch = ['零','一','二','三','四','五','六','七','八','九'] 
    num  = ['0','1','2','3','4','5','6','7','8','9']
    if len(target_ch) == 1:
        final = num[ch.index(target_ch)]
        return final
    elif len(target_ch) == 2:
        if target_ch[0] == '十':
            final = '1'+ num[ch.index(target_ch[-1])]
            return final
        else:
            final = num[ch.index(target_ch[0])] + num[ch.index(target_ch[-1])]

    elif len(target_ch) == 3:
        if target_ch.find('百') == True or target_ch.find('十') == True:
            final = num[ch.index(target_ch[0])] + num[ch.index(target_ch[-1])]
            return final
        else:
            final = num[ch.index(target_ch[0])] + num[ch.index(target_ch[1])] + num[ch.index(target_ch[2])]
            return final


    elif len(target_ch) == 4 :
        if target_ch[0] == '兩' or target_ch[0] == '二' :
            final = '2' + num[ch.index(target_ch[2])] +'0'
            return final
        else:
            final = num[ch.index(target_ch[0])]+ num[ch.index(target_ch[2])]+'0'
            return final
    elif len(target_ch) ==5 :
        if target_ch[0] == '兩' or target_ch[0] == '二' :
            final = '2' + num[ch.index(target_ch[2])] +  num[ch.index(target_ch[-1])]
            return final
        else:
            final = num[ch.index(target_ch[0])] + num[ch.index(target_ch[2])] + num[ch.index(target_ch[-1])]
            return final
    else:
        return target_ch
    



def deal_address(address):
    print('---------------修正地址開始---------------')
    after_deal = []
    for i in address:
        i = strQ2B(i)
        i = i.replace(' ','')
        regex1 = re.compile(r'\d+村') 
        regex1_2 = re.compile(r'\d+[\u4E00-\u9FFF]+村') 
        regex2 = re.compile(r'\d+里')
        regex2_2 = re.compile(r'\d+[\u4E00-\u9FFF]+里')
        regex3 = re.compile(r'\d+路')
        regex3_2 = re.compile(r'\d+[\u4E00-\u9FFF]+路')
        regex4 = re.compile(r'[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+鄰')
        regex5 = re.compile(r'[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+弄')
        regex6 = re.compile(r'[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+號')
        regex7 = re.compile(r'\d+段')
        regex8 = re.compile(r'[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+樓')       
       
        try:
            if regex1.search(i) != None:
                after_deal.append(re.sub(regex1.search(i).group()[:-1],num_to_ch(regex1.search(i).group()[:-1]),i))
                print('修正地址 :',i,'| 修正部位:',regex1.search(i).group())

            elif  regex1_2.search(i) != None:
                after_deal.append(re.sub(re.search('\d',regex1_2.search(i).group()).group(),num_to_ch(re.search('\d',regex1_2.search(i).group()).group()),i))
                print('修正地址 :',i,'| 修正部位:',re.search('\d',regex1_2.search(i).group()).group())
            
            elif  regex2.search(i) != None:
                after_deal.append(re.sub(regex2.search(i).group()[:-1],num_to_ch(regex2.search(i).group()[:-1]),i))
                print('修正地址 :',i,'| 修正部位:',regex2.search(i).group())

            elif  regex2_2.search(i) != None:
                after_deal.append(re.sub(re.search('\d',regex2_2.search(i).group()).group(),num_to_ch(re.search('\d',regex2_2.search(i).group()).group()),i))
                print('修正地址 :',i,'| 修正部位:',re.search('\d',regex2_2.search(i).group()).group())
                
            elif regex3.search(i) != None:
                after_deal.append(re.sub(regex3.search(i).group()[:-1],num_to_ch(regex3.search(i).group()[:-1]),i))
                print('修正地址 :',i,'| 修正部位:',regex3.search(i).group())

            elif regex3_2.search(i) != None:
                after_deal.append(re.sub(re.search('\d',regex3_2.search(i).group()).group(),num_to_ch(re.search('\d',regex3_2.search(i).group()).group()),i))
                print('修正地址 :',i,'| 修正部位:',re.search('\d',regex3_2.search(i).group()).group())

            elif regex4.search(i) != None:
                after_deal.append(re.sub(regex4.search(i).group()[:-1],ch_to_num(regex4.search(i).group()[:-1]),i))
                print('修正地址 :',i,'| 修正部位:',regex4.search(i).group())
            elif regex5.search(i) != None:
                after_deal.append(re.sub(regex5.search(i).group()[:-1],ch_to_num(regex5.search(i).group()[:-1]),i))
                print('修正地址 :',i,'| 修正部位:',regex5.search(i).group())
            elif regex6.search(i) != None:
                after_deal.append(re.sub(regex6.search(i).group()[:-1],ch_to_num(regex6.search(i).group()[:-1]),i))
                print('修正地址 :',i,'| 修正部位:',regex6.search(i).group())
            elif regex7.search(i) != None:
                after_deal.append(re.sub(regex7.search(i).group()[:-1],num_to_ch(regex7.search(i).group()[:-1]),i))
                print('修正地址 :',i,'| 修正部位:',regex7.search(i).group())
            elif regex8.search(i) != None:
                after_deal.append(re.sub(regex8.search(i).group()[:-1],ch_to_num(regex8.search(i).group()[:-1]),i))
                print('修正地址 :',i,'| 修正部位:',regex8.search(i).group())

            else:
                after_deal.append(i)
                
                continue
        except:
            print('修正地址 :',i,'邏輯有誤，未修正')
            after_deal.append(i)
            continue
    return after_deal

       

address = addresses_from_csv(path='test2.xlsx')
c = 0
for i in range(3):
    if c == 0:
        addresses = deal_address(address)
        c+=1
    else:
        addresses = deal_address(addresses)
        c+=1
    


api_key = 'YourAPI'

transformed = get_api(api_key,addresses)
storage_excel(address , addresses , transformed)


print('done')

