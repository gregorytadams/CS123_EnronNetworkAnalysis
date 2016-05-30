
import xml.etree.ElementTree as ET
import sys
import sqlite3
from database_funcs import open_db, commit_db

def read_and_parse(filename):
    '''
    Goes through the xmls and grabs all the en=mail metadata

    inputs: filename of xml from enron email dataset

    outputs: a dirctionary of all the emails' metadata including ID
    '''
	tree = ET.parse(filename)
	root = tree.getroot()
	d = {}
	for doc in root.iter("Document"):
		if doc.attrib['DocType'] == 'Message':
			ID = doc.attrib['DocID']
			d[ID] = {}
			for child in doc[0]:
				d[ID][child.attrib['TagName']] = {key: child.attrib[key] for key in child.attrib if key != 'TagName'}
	return d

def store_in_db(d, c, db):
    '''
    Takes metadata dictionary from read_and_parse and stores it in a database
    
    Inputs:
    d, the dictionary from read_and_parse
    c, the cursor from the database
    db, the database
    '''
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
	# print('Number partially committed: {}'.format(len(l2)))
	# print('Number not committed: {}'.format(len(l)))

def main(filename, db_path):
	c, db = open_db(db_path)
	# print(filename)
	d = read_and_parse(filename)
	store_in_db(d,c,db)
	commit_db(db)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])
	
