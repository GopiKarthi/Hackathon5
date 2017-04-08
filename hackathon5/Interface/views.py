# Create your views here.
from django.shortcuts import render_to_response

def welcome(request):
    """Welcome view to show data"""

    return render_to_response('welcome.html');
