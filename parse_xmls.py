
import xml.etree.ElementTree as ET
import sys
import sqlite3
from database_funcs import open_db, commit_db

def read_and_parse(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	d = {}
	for doc in root.iter("Document"):
		if doc.attrib['DocType'] == 'Message':
			ID = doc.attrib['DocID']
			d[ID] = {}
			for child in doc[0]: #iterates through children of <tags>
				d[ID][child.attrib['TagName']] = {key: child.attrib[key] for key in child.attrib if key != 'TagName'}
	return d #d["3.818877.G3T4II30F0UK4YM4G2XQMIIKYS451SXUA"]

def store_in_db(d, c, db):
	#c, db = open_db(db_path)
	# fields: to, from, subject, date, has_attachments
	l = []
	l2 = []
	for ID in d:
		try:
			To = d[ID]['#To']['TagValue']
			From = d[ID]['#From']['TagValue']
			Date = d[ID]['#DateSent']['TagValue']
			try:
	        		Subject = d[ID]['#Subject']['TagValue']
				HasAttachments = d[ID]['#HasAttachments']['TagValue']
			except Exception as e2:
				l2.append(e2)
				db_args = (ID, To, From, Date)
				c.execute('INSERT INTO messages (ID, SENT_TO, SENT_FROM, DATE) VALUES(?,?,?,?)', db_args)
				continue
		except Exception as e:
			l.append(e)
			continue
		db_args = (ID, To, From, Subject, Date, HasAttachments)
                c.execute('INSERT INTO messages VALUES(?,?,?,?,?,?)', db_args)

		#except Exception as e:
		#	l.append(e)
		#	continue
	print(l)
	print(l2)
	print(len(l2))
	print(len(l))
	#commit_db(db)

def main(filename, db_path):
	c, db = open_db(db_path)
	d = read_and_parse(filename)
	store_in_db(d,c,db)
	commit_db(db)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])
	
