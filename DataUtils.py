from utilities import dbconnect
import datetime
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
    for month in range(1,12):
		dict={}
		dateYYYYMM = last_day_of_month(datetime.date(year, month, 1))
		# import pdb;pdb.set_trace()
		selectMonth = str(dateYYYYMM.strftime("%Y-%m"))+"%"
		query = ("select count(*) from GetProposal where Decision='Active' and CurrentDateTime like '%s'"%selectMonth)
		# print query
		count = float(conUKLSOFT.fetch_one(query)[0])
		dict['startdate']=datetime.date(year, month, 1).strftime("%d-%b-%y")
		dict['date']=dateYYYYMM.strftime("%d-%b-%y")
		dict['Loans']=count
		print "%s till %s Loans %s"%(datetime.date(year, month, 1).strftime("%d-%b-%y"),dateYYYYMM.strftime("%d-%b-%y"),count)
		MonthlyLoans.append(dict)
	return MonthlyLoans



# ProfitYearly()
# print YearProfit
CustMothlyData()
print MonthlyLoans
