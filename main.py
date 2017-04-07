from utilities import *
import pandas
from pandas import DataFrame

con = dbconnect()
#res = con.fetch_df("select * from tracking_visitor limit 10;")
#print con.fetch_one("select * from tracking_visitor limit 10;")
#df = DataFrame(res)
#print res
print con.fetch_df("select latitude,longitude from ip_db.dbip_lookup as ip, ukllis.ClientRequest as creq where ip.ip_start=creq.IPAddr limit 5;")
#print con.fetch_df("select latitude,longitude from ip_db.dbip_lookup as ip, ukllis.ClientRequest as creq where creq.IPAddr='86.31.121.81';")
