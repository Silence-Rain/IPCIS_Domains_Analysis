#!coding=utf8

import io
import random
import math

def randResolvedIPCount():
	ret = 0
	prob = random.randint(0,10)

	if prob <= 3:
		ret = random.randint(1,2)
	elif prob <=6:
		ret = random.randint(1,10)
	else:
		ret = random.randint(1,20)

	return ret

def randTTL():
	prob = [1800,3600,3600,3600,43200,86400,86400,86400,172800,172800]
	ret = prob[random.randint(0,9)]

	return ret

def randActs_OppositeIPCount_GeoEntropy():
	acts = random.randint(10,2000)
	cnt = random.randint(math.ceil(acts/2), acts)
	entropy = round(random.randint(1,10) * random.random(),4)

	return (acts, cnt, entropy)

def randBytePerMess():
	mescnt = random.randint(10,2000)
	bytecnt = random.randint(100,20000)
	ret = round(bytecnt / mescnt,4)

	return ret

if __name__ == '__main__':
	data = []
	for i in range(0,1000):
		tup = randActs_OppositeIPCount_GeoEntropy()
		temp = [randResolvedIPCount(), randTTL(), tup[0], tup[1], tup[2], randBytePerMess()]
		data.append(temp)

	with io.open("../data/testData.csv", "w", encoding="gbk") as f:
		f.write("解析IP数,TTL,IP活动数量,对端IP数,地理分布熵,每报文字节数\r\n")

		for item in data:
			tmp = ""
			for i in range(0, 6):
				if i == 5:
					tmp += str(item[i])+"\r\n"
				else:
					tmp += str(item[i])+","

			f.write(tmp)