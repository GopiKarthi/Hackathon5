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
    data=[]

    for i in range(40):
        data.append({'date' : randomDate('1-JAN-16', '31-DEC-16', random.random()),
                     'close' : (random.random() * 500 )})


    return HttpResponse(json.dumps(data))
        
     

def MapPlot(request):
    '''Sends the data to plot the map of customers applying in UK'''
    plot_map = {'2009':'points_200912.pkl','2010':'points_201012.pkl','2011':'points_201112.pkl','2012':'points_201212.pkl','2013':'points_201312.pkl','2014':'points_201412.pkl','2015':'points_201512.pkl','2016':'points_201612.pkl'}
    year = request.GET.get("year")
    with open(plot_map[year], 'rb') as f:
        points = pickle.load(f)
    coords = get_coordinates(points)
    return HttpResponse(simplejson.dumps({'coords':coords}))
