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
        
    def byCpu(self, item):
        return item[1]
    
    def byRam(self, item):
        return item[4]
        
    def getName(self):
        return self.name
    
    def processUpdate(self):
        pInfo = []
        for proc in psutil.process_iter():                              
            memory = []
            memory.append('{:,}'.format(proc.memory_info().rss / self.mega) + " M (" + "%05.2f" % proc.memory_percent() + ")")
            memory.append('{:,}'.format(proc.memory_info().vms / self.mega) + " M")                    
            pInfo.append([proc.name(), proc.cpu_percent(), memory, proc.pid, proc.memory_info().rss] )
                    
                                
        self.processes = pInfo
        self.processes.sort(key=self.byRam, reverse=True)
        self.processes = self.processes[:5] 
        
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

    
    def update(self):
        self.processUpdate()
        self.cpuUpdate()
        self.memoryUpdate()
        

class MonitorView(TemplateView):    
    systeminfo = SyetmeInfomation()
    
    def get(self, request):        
        
        sysinfo = self.systeminfo        
        sysinfo.update() 
               
        data = { 'processes' : sysinfo.processes,
                 'cpus' : sysinfo.cpus,          
                 'memory' : sysinfo.memory,              
                 }
        return render(request, 'monitor/index.html', data)    
    
class ProcessView(TemplateView):
    
    def get(self, request, pid):
        proc = psutil.Process(int(pid))
        output = { 'name' : proc.name() ,
                  
                  }
        return render(request, 'monitor/process.html', output)
