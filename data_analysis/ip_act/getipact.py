# -*- coding: utf-8 -*
import urllib2
import time
import json
import calendar
import utils.mkdir as mkdir
import io
import glob

#传入 域名 文件夹地址，返回字典内容——文件名：(通讯记录行数,[(前三活跃的端口:记录数)])
def getIpactCount(addr):
    data={}
    read_files=glob.glob(addr+"/*.txt")

    for i in read_files:
        with open(i,'r') as infile:
            ipact=infile.readlines()
            # TODO: 端口活跃记录
            temp = {}
            # 对指定ip的所有活动记录，统计端口活跃度
            for line in ipact:
                arr = line.split(" ")
                if temp.has_key(arr[3]):
                    temp[arr[3]] += 1
                else:
                    temp[arr[3]] = 1

            res = sorted(temp.items(), key=lambda item:item[1])[:3]

        count=len(ipact)
        data[i.split("\\")[-1].split(".")[0]]=(count, res)
    return data


#传入地址，返回字典内容——域名：ip
def readIpdt(addr):
    content = None
    dict={}
    with io.open(addr, 'r', encoding='utf-8') as file:
        content = eval(file.read())
    
    return content
            
#传入域名ip字典地址和要查询的月份，将查到的ip活动信息写入到文件夹
def getIpact(data,month):
    daofmo=calendar.monthrange(2018,month)[1]

    for key,value in data.items():
        if len(value):
            #创建活动记录保存目录
            savepath='/home/lzhang/SRTP_DNS/data_analysis/data/ipact/'+key
            mkdir.mkdir(savepath)
            print key
            
            for i in range(daofmo):
                #通过url抓取Ip活动记录
                try:
                    url ="http://211.65.197.210:8080/IPCIS/activityDatabase?IpSets=%s:32&TableName=2018-%02d-%02d&Mode=2" % (value[0], month, i)  
                    response = urllib2.urlopen(url, timeout=10)   
                    html = response.read()  
                    mystr = html.decode("utf8")  
                    response.close()
                    
                    if(mystr!="{}"):
                        #将查到的ip活动记录写入到文件夹
                        file = open(savepath+'/'+str(i)+'-'+str(month)+'.txt','w') 
                        file.write(mystr) 
                        file.close()
                except Exception as e:
                    print(key, i, time.asctime(time.localtime(time.time())))
                    pass


if __name__ == "__main__":
    raw = readIpdt("../data/ipdata.txt")
    getIpact(raw, 1)
    