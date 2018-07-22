#!coding=utf8

import time
import io
import utils.datetime as datetime
from utils.mysql import MySQL

pds = []
dns_db = MySQL(host="127.0.0.1", user="root", passwd="rootofmysql", port=3307, db="IPCIS_DNS_DB")

def read_data():
	# 从文件中读取恶意域名信息
	with io.open("../data/3mths.txt", "r", encoding="latin1") as f:
		for line in f.readlines():
			temp = line.strip().split("=")
			temp[0] = temp[0].strip()
			pds.append(temp[0])

def create_db():
	sql = ("CREATE TABLE IF NOT EXISTS domain_static ( domain_id INT(10) UNSIGNED NOT NULL DEFAULT 0," 
		"primary_domain VARCHAR(128) NOT NULL DEFAULT '', "
		"is_dga INT(10) UNSIGNED NOT NULL, "
     	"ttl INT(10) UNSIGNED NOT NULL, "
     	"credit INT(10) UNSIGNED, "
	    "register_location VARCHAR(32) DEFAULT '', "
	    "register_years VARCHAR(16) DEFAULT '', "
	    "ip_active INT(10) UNSIGNED, "
	    "ip_port VARCHAR(255) DEFAULT '', "
	    "PRIMARY KEY(domain_id, primary_domain) "
	    " ) ENGINE=INNODB DEFAULT CHARSET=utf8;")

	dns_db.execute(sql)

def init_db():
	# 初始化对应的域名基本信息（原始数据）
	for item in pds:
		sql_name = ("INSERT INTO domain_static (domain_id, primary_domain, is_dga, ttl) "
			"SELECT domain_id, primary_domain, is_dga, ttl FROM domain_name "
			"WHERE primary_domain = '%s';" % item)
		
		dns_db.execute(sql_name)

	# 初始化对应的whois信息
	# sql_whois = ("UPDATE domain_detail as a INNER JOIN domain_whois as b "
	# 	"on a.primary_domain=b.primary_domain SET "
	# 	"a.registrar=b.registrar, a.registrant=b.registrant;")
	# 
	# dns_db.execute(sql_whois)

def add_register_years():
	times = []
	time_diff = []

	for item in pds:
		sql_get = ("SELECT register_date, expire_date FROM domain_whois "
		"WHERE primary_domain = '%s';") % item

		rs = dns_db.get(sql_get)

		if rs != None:
			times.append(list(rs))
		else:
			times.append([])

	for item in times:
		try:	
			temp = datetime.standard2timestamp(item[1]) - datetime.standard2timestamp(item[0])
			time_diff.append(datetime.timestamp2diff(temp))
		except:
			time_diff.append('')

	for i in range(0, len(pds)):
		sql_set = ("UPDATE domain_static SET register_years = '%s' "
		"WHERE primary_domain = '%s';") % (time_diff[i], pds[i])

		dns_db.execute(sql_set)

def add_credit_evidence():
	ret = []
	scoreDict = {"safe": 100, "unsure": 70}

	for pd in pds:
		sql = "SELECT evidence FROM domain_name WHERE primary_domain='%s';" % pd

		rs = dns_db.get(sql)

		if rs != None:
			arr = rs[0].split("\"")[2:]
			temp = None
			for item in arr:
				if item == "safe" or item == "unsure":
					temp = scoreDict[item]

			ret.append((pd, temp))
		else:
			ret.append((pd, None))

	for item in ret:
		if item[1] == None:
			sql_update = "UPDATE domain_static SET credit=NULL WHERE primary_domain='%s';" % item[0]
		else:
			sql_update = "UPDATE domain_static SET credit=%d WHERE primary_domain='%s';" % (item[1], item[0])

		dns_db.execute(sql_update)
			

if __name__ == "__main__":
	try:
		read_data()
		# create_db()
		# init_db()
		# add_register_years()
		add_credit_evidence()
	except Exception as e:
		print(e, time.asctime(time.localtime(time.time())))
	finally:
		dns_db.close()