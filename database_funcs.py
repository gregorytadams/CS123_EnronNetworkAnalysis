
import urllib.request
import json
import sqlite3

def make_url_request(url):
    '''
    opens an online connection
    '''
    response = urllib.request.urlopen(url)
    str_response = response.read().decode('utf-8')
    data = json.loads(str_response)
    return data

def open_db(path):
    '''
    Opens a connection with the database
    '''
    db = sqlite3.connect(path)
    c = db.cursor()
    return c, db

def commit_db(db):
    '''
    Saves changes and closes the database
    '''
    db.commit()
    db.close()
