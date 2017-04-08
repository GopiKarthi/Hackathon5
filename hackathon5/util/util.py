import pandas
from pandas import DataFrame
import MySQLdb
from config import *
from pickle import *

import random
import time

class dbconnect(object):
    def __init__(self,db="ukllis"):
        self.con= MySQLdb.connect(sql_host,sql_user_name,sql_pass,db)
        self.cur=self.con.cursor()
    def fetch_df(self,query):
        res = pandas.read_sql(query,con=self.con)
        return res
    def fetch_all(self,query):
        self.cur.execute(query)
        res = self.cur.fetchall()
    def fetch_one(self,query):
        self.cur.execute(query)
        res = self.cur.fetchone()
        return res
    def __del__(self):
        self.con.close()

def convert_ipv4(ip):
    return tuple(int(n) for n in ip.split('.'))

if __name__ == '__main__':
    con = dbconnect("ukllis")
    #print con.fetch_all("select * from tracking_visitor limit 10;")
    #print con.fetch_one("select * from tracking_visitor limit 10;")
    IPs = con.fetch_df("select IPAddr from ClientRequest limit 100;")
    print IPs
    try:
        print "Getting data from pickle"
        ip_data = pandas.read_pickle("ip_data_pick.pkl")
    except:
        print "Getting data from db"
        ip_data = con.fetch_df("select * from ip_db.dbip_lookup where country='GB';")
        ip_data_pick = ip_data.to_pickle("ip_data_pick.pkl")
    print "Data got"
    print ip_data
    #ip_start = ip_data['ip_start'].dropna()
    #ip_end = ip_data['ip_end'].dropna()
    plot_points = []
    for i,j in IPs.iteritems():
        input_ip = ''
        x = j.split('.')
        for p in x:
            input_ip = input_ip + "%03d"%p
        input_ip = int(input_ip)
        for m,n in ip_data['ip_start'].iteritems():
            y = ip_data['ip_start'][i].split('.')
            z = ip_data['ip_end'][i].split('.')
            start_ip = ''
            end_ip = ''
            for p in y:
                start_ip = start_ip + "%03d"%p
            for p in y:
                end_ip = start_ip + "%03d"%p
            start_ip = int(start_ip)
            end_ip = int(end_ip)
            if start_ip < input_ip and input_ip < end_ip:
                plot_points = plot_points.append([ip_data['latitude'],ip_data['longitude']])
    print plot_points



def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%d-%M-%y', prop)


