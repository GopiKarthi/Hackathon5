from utilities import *
import pandas
from pandas import DataFrame
from datetime import datetime
import pickle
import numpy as np
from random import sample

start_time = datetime.now()
con = dbconnect()
#res = con.fetch_df("select * from tracking_visitor limit 10;")
#print con.fetch_one("select * from tracking_visitor limit 10;")
#df = DataFrame(res)
#print res
#print con.fetch_df("select latitude,longitude from ip_db.dbip_lookup as ip, ukllis.ClientRequest as creq where ip.ip_start=creq.IPAddr limit 5;")
#print con.fetch_df("select latitude,longitude from ip_db.dbip_lookup as ip, ukllis.ClientRequest as creq where creq.IPAddr='86.31.121.81';")
from_date_pattern = '200912'
to_date_pattern='201001'
con = dbconnect("ukllis")
try:
    print "Getting Cres data from pickle"
    IPs = pandas.read_pickle("IPs_pick_201012.pkl")
except:
    print "Getting Cres data from db"
    #IPs = con.fetch_df("select IPAddr,ApplicationDate,Title,ReqLoanAmt,LeadID from ClientRequest limit 5;")
    IPs = con.fetch_df("select creq.IPAddr,creq.ApplicationDate,creq.Title,creq.ReqLoanAmt,creq.LeadID from ClientRequest as creq,application_agreement as app where app.id=creq.LeadID and creq.LeadID>'201012' and creq.LeadID<'201101' and app.stdSign='on';")
    IPs_pick = IPs.to_pickle("IPs_pick_201012.pkl")
    IPs = pandas.read_pickle("IPs_pick_"+from_date_pattern+".pkl")
except:
    print "Getting Cres data from db"
    #IPs = con.fetch_df("select IPAddr,ApplicationDate,Title,ReqLoanAmt,LeadID from ClientRequest limit 5;")
    IPs = con.fetch_df("select creq.IPAddr,creq.ApplicationDate,creq.Title,creq.ReqLoanAmt,creq.LeadID from ClientRequest as creq,application_agreement as app where app.id=creq.LeadID and creq.LeadID>'%s' and creq.LeadID<'%s' and app.stdSign='on';"%(from_date_pattern,to_date_pattern))
    IPs_pick = IPs.to_pickle("IPs_pick_"+from_date_pattern+".pkl")
print "IP list got"
try:
    print "Getting IP data from pickle"
    ip_data = pandas.read_pickle("ip_data_pick.pkl")
except:
    print "Getting IP data from db"
    ip_data = con.fetch_df("select * from ip_db.dbip_lookup where country='GB';")
    ip_data_pick = ip_data.to_pickle("ip_data_pick.pkl")
print "Data got"
ip_data = ip_data[ip_data['ip_start'].str.match('(.*\..*)').str.len() > 0]
print "Data cleaned"
rindex =  np.array(sample(xrange(len(IPs)), 100))
IPs = IPs.ix[rindex]
print "Data sampled for plotting"
try:
    print "Getting points from pickle"
    with open('points_'+from_date_pattern+'.pkl', 'rb') as f:
        points = pickle.load(f)
    #points = pandas.read_pickle("points.pkl")
except:
    print "Manually comparing and getting IP mapping"
    points = plot_points(IPs,ip_data)
    with open("points_"+from_date_pattern+".pkl","wb") as f:
        pickle.dump(points, f)
    #points_pick = points.to_pickle("points.pkl")
print "Scaling the coordinates"
#points = plot_points(IPs,ip_data)
coords = get_coordinates(points)
print coords
print "Execution time: ",format(datetime.now()-start_time)
