# Address-Normalization-of-Taiwan-Based-on-GoogleAPI-and-Regular-Expression

# What You Need To Do?
1.You need to apply an Google map api from :https://cloud.google.com/ .

2.You need to set excel file table name as 'address', you can reference example file : test2.xlsx


# How it work?
1. This project use Regular-Expression to deal with these addresses in first stage that make sure it conform to the Google api format.

2. It may get wrong if the fotmat is incorrect.(Example : 十三號 --> 13號 , 6段 --> 六段 , 3民路 --> 三民路)

3. In second stage use google map api to patch these addresses.

4. Folder 'Log' is for logging all processes and also error.

5. It handle blank symbols and also transform full-shaped to half-shaped.

3.This Project support .csv & .xlsx

# Result

### Orginal Data
![image](https://github.com/arleigh418/Addresses-Normalization-of-Taiwan-Based-on-GoogleAPI-and-Regular-Expression/blob/master/img/original.png)


### After First Stage
![image](https://github.com/arleigh418/Addresses-Normalization-of-Taiwan-Based-on-GoogleAPI-and-Regular-Expression/blob/master/img/first_stage.png)


### After Second Stage
![image](https://github.com/arleigh418/Addresses-Normalization-of-Taiwan-Based-on-GoogleAPI-and-Regular-Expression/blob/master/img/second_stage.png)


# Final
1.You may get some error in some special cases that are not thought of , cause I'm not very familiar with Geographical.

2.If there are some logical error , please let me know.

3.If you find any error or you have any questions,please contact we for free , welcome everyone to discuss.


