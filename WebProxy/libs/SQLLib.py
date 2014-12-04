__author__ = 'Kevin Haubris'
import sqlite3
import os


class SqlCommands:
    '''
    SQLCommands : This class is setup to house all sql queries for the sqlite database
    that is used in this script.
    Only use optDB, variable and this function if ABSOLUTLY NEEDED.
    IT MUST USE THE SAME TABLE LAYOUT AS Data/TestDB!!!
    '''
    def __init__(self, optDB = ""):
        if optDB != "":
            self.conn = sqlite3.connect(optDB)
            self.c = self.conn.cursor()
        else:
            #os.remove("Data/session.db")
            self.conn = sqlite3.connect("Data/session.db")
            self.c = self.conn.cursor()

    def CreateDB(self):
        self.c.execute("create table sites (host text, site text, requestheader text, requestdata text, responsedata text, responseheader text)")
        self.conn.commit()

    def InsertSite(self, host, site, requesthdr, requestdata, responsedata, responseheader):
        self.c.execute("insert into sites ('%s', '%s','%s','%s','%s','%s')"%(host, site, requesthdr, requestdata, responsedata, responseheader))
        self.conn.commit()

    def getSites(self):
        '''This function returns the countries that each server is in.'''
        self.c.execute("select distinct site from sites")
        servelist = self.c.fetchall()
        return servelist

    def getRequest(self, site):
        self.c.execute("select requestheader, requestdata from sites where site = '%s'" % (site))
        requests = self.c.fetchone()
        return requests