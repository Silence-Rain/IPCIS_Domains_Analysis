#!coding:utf8
#本文件用于将数据库中查阅到的服务类型分类为label文件，需要pandas库支撑

import pandas as pd

evidencePath = "../data/AlexaEvidence_10000.dat"
labelPath = "../data/AlexaLabel_10000.csv"

# 读入evidenceQueryForDatabase模块生成的evidence原始数据
# 输入格式： 	域名|evidence全体字段
# 输出格式： 	1		label
#		  	域名 	evidence
data = pd.read_table(evidencePath, sep='\'|"', names=range(0,73))
x = range(0,73)
# 域名列
x.pop(1)
# 服务类型列
x.pop(11)
# 删除其他列
data.drop(data.columns[x],axis=1, inplace=True)
# 更改服务类型列名，从12改为label
data.rename(columns={12:'label'}, inplace=True)

# 转换服务类型为label
# 输入格式： 	1	 	label
#			域名 	evidence
# 输出格式： 	1	 	label
#			域名 	1/2/3/4/5/error
cate = pd.read_csv("category/evidenceCategory_db.csv", header=None, index_col=[0,1])
dic = {}
for item in cate.iterrows():
	dic[item[0][0]] = item[0][1]
# 数据库内无服务类型或该服务类型未加入label库，设置为error
defaultItem = 'error'
# 填写Label
rows = data.iloc[:,0].size
for i in range(rows):
	data.ix[i]['label'] = dic.get(data.ix[i]['label'],defaultItem)
# 删除label值为error的行
for index,row in data.iterrows():
	if 'error' in row['label']:
		data.drop(index, axis=0, inplace=True)
 
# 写入csv文件
# 输入格式：	1	 	label
#			域名 	1/2/3/4/5
# 输出格式：	域名,label
data.to_csv(labelPath, header=None, index=None)
