import pandas
from pandas import DataFrame
import pickle
from pickle import *
from utilities import dbconnect
import datetime
import sys
import time
sys.path.append("/host/DataHack")
conTMS=dbconnect("TMS_Data")
conUKLSOFT=dbconnect("uklsoft")
YearProfit = []
MonthlyLoans = []


def ProfitYearly():
	for i in range(2011,2018):
		i = str(i)+"%"
		#count = con.fetch_one('select sum(credit) from Transactions where tran_dt like "2010%"')
		# import pdb;pdb.set_trace()
		query = ("select sum(debit)-sum(credit) from Transactions where tran_dt like '%s'"%(i))
		#print query
		#Cost of one lead is 150GBP, need to find no
		count = conTMS.fetch_one(query)
		print "Year %s Credit %s"%(i[:-1],float(count[0]))
		YearProfit.append((i[:-1],float(count[0])))
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def CustMothlyData(year=2009):
    for month in range(1,13):
		dict={}
		dateYYYYMM = last_day_of_month(datetime.date(year, month, 1))
		selectMonth = str(dateYYYYMM.strftime("%Y-%m"))+"%"
		query = ("select count(*) as Loans from GetProposal where Decision='Active' and CurrentDateTime like '%s'"%selectMonth)
		query1 = ("select sum(debit)-sum(credit) from Transactions where tran_dt like '%s'"%selectMonth)
		# q1 = "select count(Decision)as Loans,CurrentDateTime as DateTime from GetProposal where Decision='Active' and CurrentDateTime like '%s'"%selectMonth
		# # print query
		# d = con.fetch_df(q1)
		count = float(conUKLSOFT.fetch_one(query)[0])
		DbtCrt = 0.0
		# import pdb;pdb.set_trace()
		if count > 0:
			DbtCrt = float(conTMS.fetch_one(query1)[0])
			DbtCrt = DbtCrt if DbtCrt > 0.0 else 0.0
		dict['startdate']=datetime.date(year, month, 1).strftime("%d-%b-%y")
		dict['date']=dateYYYYMM.strftime("%d-%b-%y")
		dict['Loans']=count
		dict['DebitCredit']=DbtCrt
		print "%s till %s Loans %s"%(datetime.date(year, month, 1).strftime("%d-%b-%y"),dateYYYYMM.strftime("%d-%b-%y"),count)
		MonthlyLoans.append(dict)
    # import pdb;pdb.set_trace()
    with open("LoanBooked_"+dateYYYYMM.strftime("%Y")+".pkl","wb") as f:
        pickle.dump(MonthlyLoans, f)
    return MonthlyLoans




# ProfitYearly()
# print YearProfit
# for i in range(2009,2018):
#  	print "==============================================Year================================================",i
#  	CustMothlyData(i)
datas=[]
with open("/host/DataHack/LoanBooked_2017.pkl", 'rb') as f:
	datas = pickle.load(f)
accum = 0.0
profit = 0.0
for i in datas:
		accum=accum+i["Loans"]
		profit=profit+i["DebitCredit"]
		i["Loans"] = accum
		i["profit"] = profit-accum*150 # 150 is avg cost for one loan
		t = time.strptime(i['date'], '%d-%b-%y')
		now = datetime.date(2016, 1, 1)
		if t.tm_year>=now.year:
				i["Loans"],i["profit"] = 0,0

import pdb;pdb.set_trace()
print datas

# accum = 0.0
# for i in datas:
# 		accum=accum+i["Loans"]
# 		i["Loans"] = accum
#
# import pdb;pdb.set_trace()
# print datas
#print MonthlyLoans
