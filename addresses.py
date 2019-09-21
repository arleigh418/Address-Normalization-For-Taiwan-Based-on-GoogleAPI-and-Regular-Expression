# Author : Arleigh Chang
# date : 2019/09/22 Ver2.0

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


#讀取Excel，支援csv及xlsx
def addresses_from_csv(path):  
    addresses = []
    try:
        x = pd.read_excel(path,encoding = 'utf-8')
        address = x['address'].tolist()
    except:
        x = pd.read_csv(path,encoding = 'utf-8')
        address = x['address'].tolist()
    return address

#將網址傳入Google api，藉由google api進行地址補丁
def get_api(api_key , addresses ,address):
    print('---------------Google Api補丁開始---------------')
    transformed = []
    count = 0
    for query in tqdm(addresses):
        try:
            search = query.index('號')
            query_fix = query[:search+1]
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+query_fix+'sensor&language=zh-tw&key='+api_key
            r = requests.get(url,verify = False)
            data = r.json()
            try:
                if  len(query_fix)+3 - len(data['results'][0]['formatted_address'])   > 1:
                    print('地址:',query,'， 疑似異常，請檢查')    
                    transformed.append(address[count])
                    count+=1
                else:        
                    print(data['results'][0]['formatted_address'])
                    
                    transformed.append(data['results'][0]['formatted_address']+query[search+1:])
                    count+=1
            except:
                try:
                    print('於函數get_api中異常錯誤，請檢查無法解析地址:',query)
                    transformed.append(address[count])
                    count+=1
                except UnicodeEncodeError:
                    print('於函數get_api中異常錯誤，發生UnicodeEncoderError')
                    transformed.append(address[count])
                    count+=1
                    continue 
        except ValueError:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+query+'sensor&language=zh-tw&key='+api_key
            r = requests.get(url,verify = False)
            data = r.json()
            try:
                if  len(query)+3 - len(data['results'][0]['formatted_address'])   > 1:
                    print('地址:',query,'， 疑似異常，請檢查')    
                    transformed.append(address[count])
                    count+=1
                else:        
                    print(data['results'][0]['formatted_address'])
                    transformed.append(data['results'][0]['formatted_address'])
                    count+=1
                        
            except:
                try:
                    print('於函數get_api中異常錯誤，請檢查無法解析地址:',query)
                    transformed.append(address[count])
                    count+=1
                except UnicodeEncodeError:
                    print('於函數get_api中異常錯誤，發生UnicodeEncoderError')
                    transformed.append(address[count])
                    count+=1
                    continue 
      
    return transformed ,count

#儲存成Excel
def storage_excel(original_addresses , fix_addresses , final_addresses):
    try:
        print('---------------儲存檔案中--------------')
        storage = pd.DataFrame() #postcode?
        storage['original_addresses'] = original_addresses
        storage['fix_addresses'] = fix_addresses
        storage['final_addresses'] = final_addresses
        storage.to_excel('transformed_addresses123456.xlsx', encoding = 'big5' , index = False)
    except:
        print('於函數storage_excel中異常錯誤，請檢查')

#全形轉半形，此處使用 : https://www.jianshu.com/p/a5d96457c4a4 
def strQ2B(ustring): 
    ss = []
    for s in str(ustring):
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


#處理地址資料中應該是中文但是是數字的錯誤格式(數字轉中文)。支援至兩位數
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


def ch_to_num(target_ch):#處理地址資料中應該是數字但是是中文字的錯誤格式(中文轉數字)。支援至三位數
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
    



#運用正則表達式搜索錯誤格式的地址，並且運用上方轉換工具轉換成正確格式
def deal_address(address,error_code):   
    print('---------------修正地址，第',error_code,'回合開始---------------') 
    after_deal = []     
    for i in address:   
        i = strQ2B(i)
        i = i.replace(' ','')
          
        regex0 = re.compile(r'\d')
        regex0_0 = re.compile(r'[\u4e00-\u9fa5]')
        regex1 = re.compile(r'\d+村')
        regex1_2 = re.compile(r'\d+[\u4E00-\u9FFF]+村') 
        regex2 = re.compile(r'\d+里')
        regex2_2 = re.compile(r'\d+[\u4E00-\u9FFF]+里')
        regex3 = re.compile(r'\d+路')
        regex4 = re.compile(r'[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+鄰')
        regex5 = re.compile(r'[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+弄')
        regex6 = re.compile(r'[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+號')
        regex7 = re.compile(r'[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+樓')
        regex8 = re.compile(r'\d+段')
          
        try:
            if regex0.search(i[0:3]) !=None and error_code==0 and regex0_0.search(i[0:3]) ==None:
                print('修正地址 :',i,'| 修正部位:',i[0:3])
                after_deal.append(i.replace(i[0:3],''))

            elif regex0.search(i[0:5]) !=None and error_code==1 and regex0_0.search(i[0:5]) ==None:
                print('修正地址 :',i,'| 修正部位:',i[0:5])
                after_deal.append(i.replace(i[0:5],''))
                
      
            elif regex0_0.search(i[0:5]) !=None and error_code==2 and regex0_0.search(i[0:5]) ==None:
                print('修正地址 :',i,'| 修正部位:',i[0:5])
                after_deal.append(i.replace(i[0:5],''))
        
    
            elif regex1.search(i) != None and error_code==3:
                after_deal.append(re.sub(regex1.search(i).group()[:-1],num_to_ch(regex1.search(i).group()[:-1]),i))
                print('修正地址 :',i,'| 修正部位:',regex1.search(i).group())
                 

            elif  regex1_2.search(i) != None and error_code==4:
                print('修正地址 :',i,'| 修正部位:',re.search('\d',regex1_2.search(i).group()).group())
                after_deal.append(re.sub(re.search('\d',regex1_2.search(i).group()).group(),num_to_ch(re.search('\d',regex1_2.search(i).group()).group()),i))
                
                         
            elif  regex2.search(i) != None and error_code==5:
                print('修正地址 :',i,'| 修正部位:',regex2.search(i).group())
                after_deal.append(re.sub(regex2.search(i).group()[:-1],num_to_ch(regex2.search(i).group()[:-1]),i))
                
               

            elif  regex2_2.search(i) != None and error_code==6:
                print('修正地址 :',i,'| 修正部位:',re.search('\d',regex2_2.search(i).group()).group())
                after_deal.append(re.sub(re.search('\d',regex2_2.search(i).group()).group(),num_to_ch(re.search('\d',regex2_2.search(i).group()).group()),i))
                
                
                
            elif regex3.search(i) != None and error_code==7:
                print('修正地址 :',i,'| 修正部位:',regex3.search(i).group())
                after_deal.append(re.sub(regex3.search(i).group()[:-1],num_to_ch(regex3.search(i).group()[:-1]),i))
                
               

            elif regex4.search(i) != None and error_code==8:
                print('修正地址 :',i,'| 修正部位:',regex4.search(i).group())
                after_deal.append(re.sub(regex4.search(i).group()[:-1],ch_to_num(regex4.search(i).group()[:-1]),i))
                
                

            elif regex5.search(i) != None and error_code==9:
                print('修正地址 :',i,'| 修正部位:',regex5.search(i).group())
                after_deal.append(re.sub(regex5.search(i).group()[:-1],ch_to_num(regex5.search(i).group()[:-1]),i))
                
               

            elif regex6.search(i) != None and error_code==10:
                print('修正地址 :',i,'| 修正部位:',regex6.search(i).group())
                after_deal.append(re.sub(regex6.search(i).group()[:-1],ch_to_num(regex6.search(i).group()[:-1]),i))
                
                

            elif regex7.search(i) != None and error_code==11:
                print('修正地址 :',i,'| 修正部位:',regex7.search(i).group())
                after_deal.append(re.sub(regex7.search(i).group()[:-1],ch_to_num(regex7.search(i).group()[:-1]),i))
                
            

            elif regex8.search(i) != None and error_code==12:
                after_deal.append(re.sub(regex8.search(i).group()[:-1],num_to_ch(regex8.search(i).group()[:-1]),i,1))
                
                print('修正地址 :',i,'| 修正部位:',regex8.search(i).group())
                         
            else:
                after_deal.append(i)
                continue

        except TypeError:
            print('修正地址 :',i,'邏輯有誤，未修正')
            after_deal.append(i)
            continue
    error_code+=1
    return after_deal , error_code


address = addresses_from_csv(path='test2.xlsx')
c = 0
error_code = 0
for i in range(0,15):
    if c == 0:    
        addresses,error_code = deal_address(address,error_code)
        c+=1
       
    elif c !=0 and error_code !=0:
        addresses , error_code = deal_address(addresses,error_code)
        c+=1
    else:
        break
    

api_key = 'Yourkey'

transformed,error = get_api(api_key,addresses,address)

storage_excel(address , addresses , transformed)

print('done')

