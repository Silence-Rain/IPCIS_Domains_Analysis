import time
import math

def standard2timestamp(str_time):
	tm = time.strptime(str_time, '%d-%b-%Y')
	return int(time.mktime(tm))

def timestamp2diff(int_time):
	y = int(math.floor(int_time / 31536000))
	m = int(math.floor((int_time - 31536000 * y) / 2592000))
	d = int(math.floor((int_time - 31536000 * y - 2592000 * m) / 86400))

	return "%s-%s-%s" % (y, m, d)