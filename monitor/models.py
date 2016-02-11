from __future__ import unicode_literals

from django.db import models

import psutil

class Data:
    cpu_clock = 0
    
    def __init__(self):
        self.name = 'test'
        
    def getName(self):
        return self.name
    
    def update(self):
        self.cpu_clock = psutil.cpu_percent()
        
    def getCPUClock(self):
        return self.cpu_clock
    


class Monitor(models.Model):        
    data = Data()
    
    def __str__ (self):
        return self.name
    
    