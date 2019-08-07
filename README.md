# Taiwan-Addresses-Normalization-Based-on-GoogleAPI-and-Regular-Expression

# What You Need ?
1.You need to apply an Google map api from :https://cloud.google.com/ .

2.You need to set excel file table name as 'address', you can reference example file : test2.xlsx

3.This project support .csv and .xlsx .

# How it work?
1. This project use Regular-Expression to deal with these addresses in first stage that make sure it conform to the Google api format.

2. It may get wrong if the fotmat is incorrect.(Example : 十三號 --> 13號 , 6段 --> 六段 , 3民路 --> 三民路)

3. In second stage use google map api to patch these addresses.

4. Folder 'Log' is for logging all processes and also error.

5. It handle blank symbols and also transform full-shaped to half-shaped.

# Result
![image](https://github.com/arleigh418/Automatic-IG-Like/blob/master/example/example.gif)


