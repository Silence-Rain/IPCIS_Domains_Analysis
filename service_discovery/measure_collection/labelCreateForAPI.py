#!coding:utf8
#本文件用于将VirusTotalAPI中查阅到的服务类型分类为label文件

import pandas as pd

evidencePath = "../data/MaliciousEvidence_10000.dat"
labelPath = "../data/MaliciousLabel_10000.csv"

# 读入evidenceQueryForAPI生成的evidence原始数据
# 输入格式：	域名|evidence
# 输出格式： 	0		label
# 			域名 	evidence
data = pd.read_table(evidencePath, sep='|', names=(0,1))
data.rename(columns={1:'label'}, inplace=True)#更改服务类型列名，从1改为label

# 转换服务类型为label
# 输入格式： 	0		label
#			域名 	evidence
# 输出格式： 	0		label
#			域名		1/2/3/4/5/error
cate = pd.read_csv("category/evidenceCategory_api.csv", header=None, index_col=[0,1])
dic = {}
for item in cate.iterrows():
	dic[item[0][0]] = item[0][1]
# 数据库内无服务类型或该服务类型未加入label库，设置为error
defaultItem = 'error'
# 填写Label
rows = data.iloc[:,0].size
for i in range(rows):
	data.ix[i]['label'] = dic.get(data.ix[i]['label'],defaultItem)
#删除label值为error的行
for index,row in data.iterrows():
	if 'error' in row['label']:
		data.drop(index, axis=0, inplace=True)
 
# 写入csv文件
# 输入格式：	0		label
#			域名 	1/2/3/4/5
# 输出格式：	域名,label
data.to_csv(labelPath, header=None, index=None)
