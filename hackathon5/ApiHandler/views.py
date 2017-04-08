# Create your views here.
import json
from datetime import datetime as dt
from django.http import HttpResponse
import random

from util.util import dbconnect, randomDate

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
        
     
