#!coding=utf8

import numpy as np
from OS_ELM import OS_ELM
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

# 0-1归一化
# @param x {np.float} 当前值
# @param min {np.float} 最小值
# @param max {np.float} 最大值
# @return {np.float} 归一化后的值
def zeroone(x, min, max):
	return (x - min) / (max - min)

# 获取一组离散数据的所有取值，并按照出现频率降序排序
# @param data {np.array} 一维的离散数据
# @return {list} [数据, 出现次数]的列表
def get_range(data):
	arr = []
	freq = []

	for item in data:
		if item not in arr:
			arr.append(item)
			freq.append(1)
		else:
			freq[arr.index(item)] += 1
	for i in range(0, len(arr)):
		arr[i] = [arr[i], freq[i]]
	arr.sort(key=lambda x:x[1], reverse=True)

	return arr

# 对数据进行归一化处理
# ttl值，平均流长：使用0-1归一化
# 通信协议类型，端口：使用one-hot编码，出现次数小于3次的所有值类型取为-1
def normalize(data):
	ret = [[item[0]] for item in data]
	# 0-1归一化处理ttl值与平均流长
	max_ttl = np.max(data[:,1:2])
	min_ttl = np.min(data[:,1:2])
	max_avrlen = np.max(data[:,4:5])
	min_avrlen = np.min(data[:,4:5])
	for index, row in enumerate(data):
		ret[index].append(zeroone(row[1], min_ttl, max_ttl))
		ret[index].append(zeroone(row[4], min_avrlen, max_avrlen))

	# one-hot编码处理通信协议类型与端口
	port = [int(x[2]) for x in data]
	transType = [int(x[3]) for x in data]
	port_range = get_range(port)
	type_range = get_range(transType)
	# 将出现次数小于3次的离散值统一设置为-1
	ignores = []
	for item in port_range:
		if item[1] < 3:
			ignores.append(item[0])
	for item in ignores:
		for i in range(len(port)):
			if port[i] == item:
				port[i] = 100000
	# enc_port = OneHotEncoder()
	# enc_type = OneHotEncoder()
	# enc_port.fit([[x] for x in port])
	# enc_type.fit([[x] for x in transType])
	# for i in range(len(data)):
	# 	ret[i].extend(enc_port.transform([[port[i]]]).toarray().tolist()[0])
	# 	ret[i].extend(enc_type.transform([[transType[i]]]).toarray().tolist()[0])
	enc_port = LabelEncoder()
	enc_type = LabelEncoder()
	enc_port.fit([x for x in port])
	enc_type.fit([x for x in transType])
	for i in range(len(data)):
		ret[i].extend(enc_port.transform([port[i]]))
		ret[i].extend(enc_type.transform([transType[i]]))

	return np.array(ret)


if __name__ == '__main__':
	# 读取数据
	raw = np.loadtxt(open("../data/FinalMeasures.csv", "r"), delimiter=",")
	# 归一化数据
	data = normalize(raw)
	# 按照4:1的比例分配训练集和测试集
	train = data[:100]
	test = data[1000:]
	# 设置模型参数：
	# 隐层节点：150
	# 输入节点：12
	# 模型id：test_model
	# 不进行归一化处理（原始数据已经归一化）
	elm = OS_ELM(hidden_neuron=40, input_neuron=4, id="test_model", norm="no")
	# 训练模型
	network = elm.fit_init(data=train)
	# # 输出模型预测结果
	# res = network.predict(data=test[:,1:])
