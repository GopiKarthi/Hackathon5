import pandas
from pandas import DataFrame
import MySQLdb
from config import *
from pickle import *
from netaddr import *
from itertools import izip
import datetime

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

def plot_points(IPs,ip_data):
    plot_points = []
    for i,j in enumerate(IPs.itertuples(index=True),1):
        try:
            input_ip = int(IPAddress(j[1]))
            for m,n in enumerate(ip_data.itertuples(index=True),1):
                try:
                    start_ip = int(IPAddress(n[1]))
                    end_ip = int(IPAddress(n[2]))
                    if start_ip < input_ip < end_ip:
                        plot_points.append([n[8],n[9],j[1],j[2],j[3],j[4]])
                        print j[5]
                        break
                except:
                    pass
        except:
            pass
    return plot_points

def get_coordinates(points):
    print points
    xfactor = 67.38768718802
    xoffset = 737.46256239601
    yfactor = -115.3701968135
    yoffset = 7021.9709465792
    coords = []
    for i in points:
        x = (float(i[1]) * xfactor) + xoffset
        y = (float(i[0]) * yfactor) + yoffset;
        coords.append([x,y,datetime.datetime.strftime(i[3],'%d-%m-%Y'),'Male' if i[4]=='Mr' else 'Female',i[5]])
    return coords

if __name__ == '__main__':
    con = dbconnect("ukllis")
    #print con.fetch_all("select * from tracking_visitor limit 10;")
    #print con.fetch_one("select * from tracking_visitor limit 10;")
    IPs = con.fetch_df("select IPAddr from ClientRequest limit 5;")
    print "IP list got"
    try:
        print "Getting data from pickle"
        ip_data = pandas.read_pickle("ip_data_pick.pkl")
    except:
        print "Getting data from db"
        ip_data = con.fetch_df("select * from ip_db.dbip_lookup where country='GB';")
        ip_data_pick = ip_data.to_pickle("ip_data_pick.pkl")
    print "Data got"
    ip_data = ip_data[ip_data['ip_start'].str.match('(.*\..*)').str.len() > 0]
    print "Data cleaned"
    #print ip_data
    #ip_start = ip_data['ip_start'].dropna()
    #ip_end = ip_data['ip_end'].dropna()
    plot_points = []
    for i,j in IPs['IPAddr'].iteritems():
        input_ip = ''
        x = j.split('.')
        for p in x:
            input_ip = input_ip + "%03d"%int(p)
        input_ip = int(input_ip)
        for m,n in ip_data['ip_start'].iteritems():
            y = ip_data['ip_start'][m].split('.')
            z = ip_data['ip_end'][m].split('.')
            start_ip = ''
            end_ip = ''
            for p in y:
                start_ip = start_ip + "%03d"%int(p)
            for p in z:
                end_ip = end_ip + "%03d"%int(p)
            start_ip = int(start_ip)
            end_ip = int(end_ip)
            #print "start_ip ", start_ip
            #print "input_ip ", input_ip
            #print "end_ip ", end_ip
            if start_ip < input_ip and input_ip < end_ip:
                plot_points.append([ip_data['latitude'][m],ip_data['longitude'][m]])
                print "Plotting:",ip_data['latitude'][m],", ",ip_data['longitude'][m],"\n"
                break
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
    return strTimeProp(start, end, '%d-%b-%y', prop)

