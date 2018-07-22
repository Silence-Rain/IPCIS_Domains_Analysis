from mysql import MySQL
import urllib2
import csv
import datetime
import math

db = MySQL(
	host="127.0.0.1",
	user="root",
	passwd="rootofmysql",
	port=3307,
	db="IPCIS_DNS_DB"
	)

# IP整型与字符串转换
# @param x {int} 整型IP
# @return {string} 字符串型IP
num2ip = lambda x: '.'.join([str(math.floor(x/(256**i)%256)) for i in range(3,-1,-1)])

# 读取域名及服务类型
# @param path {string} 文件路径
# @return {dict} 域名，服务类型映射，{域名: 服务类型}
def read_file(path):
	ret = {}
	with open(path,'rb') as csvfile:
		for row in csv.reader(csvfile):
			ret[row[0].strip()] = row[1]
	return ret

# 查询IP流记录中的端口号，协议类型，平均流长
# @param ip {string} 字符串型IP
# @param date {string} 日期字符串
# @return {tuple} 端口号，协议类型，平均流长
def get_ip_activity(ip, date):
	url = "http://211.65.197.210:8080/IPCIS/activityDatabase/?IpSets=%s:32&TableName=%s&Mode=2" % (ip, date)
	response = urllib2.urlopen(url)   
	html = response.read()  
	response.close()
	ip_act_dic = eval(html)

	if ip_act_dic:
		for k,v in ip_act_dic.items():
			ip_info = v[0][0].split()
			if ip_info:
				port = ip_info[2]
				transferType = ip_info[4]
				byte = int(ip_info[11]) / int(ip_info[14])
				return port, transferType , averlen
			else:
				return -1,-1,-1
	else:
		return -1,-1,-1

# 查询DNS库中域名ttl值（只取第一个）
# @param domain {string} 域名
# @return {int} ttl值
def get_ttl(domain):
	sql = "SELECT ttl FROM domain_name WHERE primary_domain = '%s';" % domain
	result = db.get(sql)
	if result:
		return result[0]
	else:
		return -1

# 获取域名所有测度信息
# @param data {dict} 域名，服务类型映射，{域名: 服务类型}
# @return {dict} 解析IP，测度映射，{解析IP：[服务类型，ttl，端口，协议类型，平均流长]}
def get_measures(data):
	ret = {}
	today = datetime.date.today()
	for k, v in data:
		# 查询ttl
		ttl = get_ttl(k)
		# 查询域名对应的解析IP
		sql = "SELECT domain_id FROM domain_name WHERE primary_domain = '%s';" % k
		domain_id = db.get(sql)[0]
		sql = "SELECT ip FROM resolved_ip WHERE domain_id = '%s' LIMIT 1" % domain_id
		ip = db.get(sql)
		# 查询IP流记录中的测度
		if ip:
			# 查询最近20天内最晚的记录
			for d in range(20):
				date = today - datetime.timedelta(days=19 - d)
				port,transferType,averlen = get_ip_activity(num2ip(ip1),str(date))
				if port != -1:
					break
				else:
					continue
		else:
			port,transferType,averlen = -1,-1,-1
		# 如果流记录查询未查询到，则过滤该域名
		if port == -1:
			continue
		
		ret[ip]=[v, ttl, port, transferType, averlen]

	return ret

# 测度结果（服务类型，ttl，端口，协议类型，平均流长）写入文件
# @param path {string} 输出文件路径
# @param data {dict} 测度结果字典
def write_file(path, data):
	with open(path,'w') as f:
		for k,v in data.items():
			for item in v:
				f.write(str(item) + ",")
			f.write("\n")


if __name__ == '__main__':
	rfile = "../data/AlexaLabel_10000.csv"
	wfile = "../data/AlexaMeasures_10000.csv"
	raw = read_file(rfile)
	measures = get_measures(raw)
	write_file(wfile, measures)
	