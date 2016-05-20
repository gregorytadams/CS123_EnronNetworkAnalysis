
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
	for ID in d:
		To = d[ID]['#To']['TagValue']
		From = d[ID]['#From']['TagValue']
		Subject = d[ID]['#Subject']['TagValue']
		Date = d[ID]['#DateSent']['TagValue']
		HasAttachments = d[ID]['#HasAttachments']['TagValue']
		
		db_args = (ID, To, From, Subject, Date, HasAttachments)
		c.execute('INSERT INTO messages VALUES(?,?,?,?,?,?)', db_args)
	#commit_db(db)

def main(filename, db_path):
	c, db = open_db()
	read_and_parse(filename)
	
	print(read_and_parse(filename))
	commit_db(db)
if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])
	
