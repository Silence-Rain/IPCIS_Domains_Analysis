#coding: utf8

import MySQLdb

class MySQL(object):
	def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
		self.conn = MySQLdb.connect(
						host = host, 
						port = port, 
						user = user,
						passwd = passwd,
						db = db,
						charset = charset
						)
		self.cursor = self.conn.cursor()

	def query(self, sql, mode=0):
		self.cursor.execute(sql)

		if mode == 0:
			return self.cursor.fetchall()
		else:
			return self.cursor.fetchone()

	def execute(self, sql):
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except Exception as e:
			self.conn.rollback()

	def close(self):
		self.cursor.close()
		self.conn.close()