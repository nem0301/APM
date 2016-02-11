from django.shortcuts import render
from models import Monitor

def index (request):
    model = Monitor     
    model.data.update()
    data = { 'data' : model.data.getCPUClock() }
    return render(request, 'APM/index.html', data)
