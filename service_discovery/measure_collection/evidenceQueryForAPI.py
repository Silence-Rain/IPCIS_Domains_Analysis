#--coding=utf-8--
#本文件用于定时查询VirusTotal网站所提供的evidence字段,VirusToal同一个apikey限制15s查询一次
import pandas as pd
import json
import urllib
import time
primary_domain=[]
evidence=[]
api_key = "647240477c2e0a60e877a89159d1af43cc833396beb922d856e8fee5c19e67cc"

# 调用virustotal.com API查询服务类型
# @param domain {string} 域名
# @return {string} 服务类型
def query(domain):
	url = 'https://www.virustotal.com/vtapi/v2/domain/report'
	parameters = {'domain': domain, 'apikey': api_key}
	response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(parameters))).read()
	response_dict = json.loads(response)

	return response_dict['Forcepoint ThreatSeeker category']

# 按行读入域名文件
# @param path {string} 域名文件路径
# @return {list} 域名列表
def read_file(path):
	ret = []
	with open(path, "r") as f:
		for line in f.readlines():
			ret.append(line.strip())
	return ret

# 每隔15秒查询一个域名的服务类型（受virustotal.com限制）
# @param domains {list} 域名列表
# @return {list} (域名,服务类型)元组的列表
def get_evidence(domains):
	ret = []
	for item in domains:
		try:
			time.sleep(15)
			evidence = query(item)
			if evidence:
				ret.append(item, evidence)
		except Exception as e:
			continue
	return ret

# 查询结果写入文件
# @param path {string} 写入文件路径
# @param data {list} (域名,evidence)元组的列表
def write_file(path, data):
	with open(path, "w") as f:
		for item in data:
			f.write("%s|%s\n" % item)


if __name__ == '__main__':
	rfile = "../data/Malicious_10000.dat"
	wfile = "../data/MaliciousEvidence_10000.dat"
	domains = read_file(rfile)
	evidence = get_evidence(domains)
	write_file(wfile, evidence)

