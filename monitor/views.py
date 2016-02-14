from django.shortcuts import render
from models import Monitor
from django.views.generic.base import TemplateView
import psutil

class SyetmeInfomation:
    
    kilo = 1024
    mega = kilo * kilo
    giga = mega * kilo  
    
    def __init__(self):
        self.name = 'test'
        self.processes = []
        self.cpus = []
        self.memory = []        
        self.sortedMethod = ''
        
    def byCpu(self, item):
        return item[1]
    
    def byRam(self, item):
        return (item[2])[0]
        
    def getName(self):
        return self.name
    
    def processUpdate(self, parsedData):
        pInfo = []
        for proc in psutil.process_iter():
            for each in parsedData:
                if proc.name() == each:  
                    memory = []
                    memory.append('{:,}'.format(proc.memory_info().rss / self.mega))
                    memory.append('{:,}'.format(proc.memory_info().vms / self.mega))                    
                    pInfo.append([proc.name(), proc.cpu_percent(), memory])
                    break
                                
        self.processes = pInfo        
        if self.sortedMethod == 'ramdesc' :
            self.processes.sort(key=self.byRam, reverse=True)
        else :
            self.processes.sort(key=self.byCpu, reverse=True)
        
    def cpuUpdate(self):
        self.cpus = []
        cores = psutil.cpu_percent(percpu=True)
        for core in range(len(cores)):
            self.cpus.append([core, cores[core]])
            
    def memoryUpdate(self):
        memory = psutil.virtual_memory()
        
        self.memory = []
        self.memory.append('{:,}'.format(int(memory.total / self.mega)))
        self.memory.append('{:,}'.format(int(memory.available / self.mega)))
        self.memory.append('{:,}'.format(int(memory.active / self.mega)))

    
    def update(self, parsedData):
        self.processUpdate(parsedData)
        self.cpuUpdate()
        self.memoryUpdate()
        

class MonitorView(TemplateView):    
    systeminfo = SyetmeInfomation()
    
    def get(self, request):
        parsedData = request.path
        parsedData = parsedData.replace(" ", "").replace("/", "")
        parsedData = parsedData.split(",")
        
        sysinfo = self.systeminfo
        sysinfo.sortedMethod = parsedData[0]
        sysinfo.update(parsedData[1:]) 
               
        data = { 'processes' : sysinfo.processes,
                 'cpus' : sysinfo.cpus,          
                 'memory' : sysinfo.memory,              
                 }
        return render(request, 'monitor/index.html', data)
    
