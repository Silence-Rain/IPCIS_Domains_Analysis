#!coding:utf8
from mysql import MySQL

db = MySQL(
	host="127.0.0.1",
	user="root",
	passwd="rootofmysql",
	port=3307,
	db="IPCIS_DNS_DB"
	)

# 按行读入域名文件
# @param path {string} 域名文件路径
# @return {list} 域名列表
def read_file(path):
	ret = []
	with open(path, "r") as f:
		for line in f.readlines():
			ret.append(line.strip())
	return ret

# 查询DNS库中域名对应的evidence字段
# @param domains {list} 域名列表
# @return {list} (域名,evidence)元组的列表
def get_evidence(domains):
	ret = []
	for item in primary_domain:
		sql = "SELECT primary_domain,evidence FROM domain_name WHERE primary_domain = '%s' " % item
		res = db.get(sql)
		ret.append(res)
	return ret

# 查询结果写入文件
# @param path {string} 写入文件路径
# @param data {list} (域名,evidence)元组的列表
def write_file(path, data):
	with open(path, "w") as f:
		for item in data:
			f.write("%s|%s\n" % item)


if __name__ == '__main__':
	rfile = "../data/Alexa_10000.dat"
	wfile = "../data/AlexaEvidence_10000.dat"
	domains = read_file(rfile)
	evidence = get_evidence(domains)
	write_file(wfile, evidence)
