# Create your views here.
import json
from datetime import datetime as dt
from django.http import HttpResponse
import random
from util.util import dbconnect, randomDate
import pickle
from util.util import *
from hackathon5 import *
import simplejson
import sys
sys.path.append("/host/DataHack/")

def AppRateReal(request):
    """To calculate and return the Application rate
    Realtime"""

    #if not request.method == 'POST':
    #    return HttpResponse('Method not allowed', status=402)

    #req_type = request.POST.get('type', '')

    #if req_type == 'all':
    q= """select count(*) from application_application where id like "%s%%";"""%dt.strftime(dt.now(),'%Y%d%m%H')

    dbconnect

    return HttpResponse(q)



def CustData(request):
    datas=[]

    # for i in range(10):
    #     data.append({'date' : randomDate('1-Jan-16', '31-Dec-16', random.random()),
    #                  'close' : (random.random() * 500 )})

    # for year in range(2009,int(request.GET.get("y"))+1):
    with open("/host/DataHack/LoanBooked_"+request.GET.get("y")+".pkl", 'rb') as f:
        datas = pickle.load(f)
    accum = 0.0
    profit = 0.0
    for i in datas:
    		accum=accum+i["Loans"]
            profit=profit+i["DebitCredit"]
    		i["Loans"] = accum
            i["profit"] = profit-accum*150 # 150 is avg cost for one loan
    return HttpResponse(json.dumps(datas))



def MapPlot(request):
    '''Sends the data to plot the map of customers applying in UK'''
    plot_map = {'2009':'points_200912.pkl','2010':'points_201012.pkl','2011':'points_201112.pkl','2012':'points_201212.pkl','2013':'points_201312.pkl','2014':'points_201412.pkl','2015':'points_201512.pkl','2016':'points_201612.pkl'}
    year = request.GET.get("year")
    with open(plot_map[year], 'rb') as f:
        points = pickle.load(f)
    coords = get_coordinates(points)
    male = 0
    female = 0
    for i in coords:
        if i[3] == 'Male':
            male = male + 1
        else:
            female = female + 1
    total_cust = male + female
    male_percent = (float(male)/float(total_cust)) * 100
    female_percent = (float(female)/float(total_cust)) * 100
    male_percent = '%.2f' % male_percent
    female_percent = '%.2f' % female_percent
    return HttpResponse(simplejson.dumps({'coords':coords,'male':str(male_percent)+'%','female':str(female_percent)+'%'}))
