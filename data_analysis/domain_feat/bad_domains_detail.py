#!coding=utf8

# import mysql
import io
import plot as plt
from collections import OrderedDict

res = []
res_whois = []
res_ttl = []

def read_raw():
	with io.open("../data/3mths.txt", "r", encoding="utf8") as f:
		for line in f.readlines():
			temp = line.strip().split("=")
			temp[0] = temp[0].strip()
			temp[1] = temp[1].split(",")

			res.append(temp)

def get_whois():
	with io.open("../data/3mths_whois.txt", "w") as f:
		for item in res:
			sql = "select * from domain_whois where primary_domain='%s';" % item[0]
			mysql.cursor.execute(sql)
			rs = mysql.cursor.fetchone()

			if rs is None:
				pass
			else:
				res_whois.append(rs)

		for item in res_whois:
			f.write(str(item) + "\n")

def get_ttl():
	with io.open("../data/3mths_ttl.txt", "w") as f:
		for item in res:
			sql = "select primary_domain,is_dga,ttl from domain_name where primary_domain='%s';" % item[0]
			mysql.cursor.execute(sql)
			rs = mysql.cursor.fetchone()

			if rs is None:
				pass
			else:
				res_ttl.append(rs)

		for item in res_ttl:
			f.write(str(item) + "\n")

def dga_percentage():
	cnt = 0
	dga_dist = [0,0]

	with io.open("../data/3mths_ttl.txt", "r") as f:
		for line in f.readlines():
			temp = tuple(eval(line))
			cnt += 1

			if temp[1] == 0:
				dga_dist[0] += 1
			else:
				dga_dist[1] += 1

	dga_dist[0] /= cnt/100
	dga_dist[1] /= cnt/100

	plt.plot_pie(dga_dist)

def ttl_bar():
	ttl_dist = OrderedDict()
	raw = []

	with io.open("../data/3mths_ttl.txt", "r") as f:
		for line in f.readlines():
			raw.append(int(tuple(eval(line))[2]))

	for i in range(0, 12):
		index = str(i * 300) + '-' + str((i + 1) * 300 - 1)
		ttl_dist[index] = 0

		for item in raw:
			if item >= i * 300 and item < (i + 1) * 300:
				ttl_dist[index] += 1

	for i in range(0, 12):
		index = str(3600 + i * 600) + '-' + str(3600 + (i + 1) * 600 - 1)
		ttl_dist[index] = 0

		for item in raw:
			if item >= 3600 + i * 600 and item < 3600 + (i + 1) * 600:
				ttl_dist[index] += 1

	for i in range(0, 40):
		index = str(14400 + i * 1800) + '-' + str(14400 + (i + 1) * 1800 - 1)
		ttl_dist[index] = 0

		for item in raw:
			if item >= 14400 + i * 1800 and item < 14400 + (i + 1) * 1800:
				ttl_dist[index] += 1

	for i in range(0, 24):
		index = str(86400 + i * 3600) + '-' + str(86400 + (i + 1) * 3600 - 1)
		ttl_dist[index] = 0

		for item in raw:
			if item >= 86400 + i * 3600 and item < 86400 + (i + 1) * 3600:
				ttl_dist[index] += 1

	for i in range(0, 8):
		index = str(172800 + i * 21600) + '-' + str(172800 + (i + 1) * 21600 - 1)
		ttl_dist[index] = 0

		for item in raw:
			if item >= 172800 + i * 21600 and item < 172800 + (i + 1) * 21600:
				ttl_dist[index] += 1

	ttl_dist['345600-604799'] = 0
	for item in raw:
		if item >= 345600 and item < 604799:
			ttl_dist['345600-604799'] += 1

	ttl_dist['604800-1799999'] = 0
	for item in raw:
		if item >= 604800 and item < 1799999:
			ttl_dist['604800-1799999'] += 1

	ttl_dist['1800000-3599999'] = 0
	for item in raw:
		if item >= 1800000 and item < 3599999:
			ttl_dist['1800000-3599999'] += 1

	ttl_dist['3600000-10000000'] = 0
	for item in raw:
		if item >= 3600000 and item < 10000000:
			ttl_dist['3600000-10000000'] += 1

	ttl_dist['10000000-'] = 0
	for item in raw:
		if item >= 10000000:
			ttl_dist['10000000-'] += 1


	plt.plot_bar(ttl_dist)

if __name__ == "__main__":
	# read_raw()
	# get_whois()
	# get_ttl()
	# dga_percentage()
	ttl_bar()
