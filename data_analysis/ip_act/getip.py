# !/usr/bin/env python
# -*- coding:utf-8 -*-

from utils.mysql import MySQL
import os  
import socket
import struct

dns_db = MySQL(host="127.0.0.1", user="root", passwd="rootofmysql", port=3307, db="IPCIS_DNS_DB")
file = open('./3mths.txt') 

#获取域名列表
name_list = []  
for  line in  file.readlines(): 
         name_list.extend(line.split("=")[1].split(",")[0:-1:1])

#去除列表中元素的空格
for i in range(len(name_list)):
     name_list[i]=name_list[i].strip()   
     
file.close()

#ip字典
ip_dic = {}

# SQL 查询语句
for name in name_list :
   sql = "select ip from resolved_ip where domain_name='"+name+"';"   
   
   #fetchall:获取ip的数据
   ip = dns_db.query(sql)
   if len(ip) !=0:
       ip = list(ip[0])
   else:
       ip = []
       
   for i in range(len(ip)):
       ip[i] = socket.inet_ntoa(struct.pack('!I',ip[i]))
       
   ip_dic[name]=ip


#保存ip字典
file = open('./ipdata.txt','w') 
file.write(str(ip_dic))  
file.close()  


#关闭连接
dns_db.close()