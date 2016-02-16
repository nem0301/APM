from django.shortcuts import render
from models import Monitor
from django.views.generic.base import TemplateView
import psutil, datetime

class SyetmeInfomation:
    
    kilo = 1024
    mega = kilo * kilo
    giga = mega * kilo  
    
    def __init__(self):
        self.name = 'test'
        self.processes = []
        self.cpus = []
        self.memory = {}        
        
    def byCpu(self, item):
        return item['cpu_percent']
    
    def byRam(self, item):
        return item['mem_percent']
        
    def getName(self):
        return self.name
    
    def processUpdate(self):
        pInfo = []
        for proc in psutil.process_iter():            
            memory = {'rss' : '{:,}'.format(proc.memory_info().rss / self.mega),
                      'vms' : '{:,}'.format(proc.memory_info().vms / self.mega), 
                      }
            proc = {'name' : proc.name(),
                    'pid' : proc.pid, 
                    'cpu_percent' : proc.cpu_percent(), 
                    'memory' : memory,              
                    'mem_percent' : "%05.2f" % proc.memory_percent(),
                    }                   
            pInfo.append(proc)
                    
                                
        self.processes = pInfo
        self.processes.sort(key=self.byRam, reverse=True)
        self.processes = self.processes[:5] 
        
    def cpuUpdate(self):
        self.cpus = []
        cores = psutil.cpu_percent(percpu=True)
        for core in range(len(cores)):
            self.cpus.append( {'numOfCore' : core, 
                               'clock' :cores[core],
                               }
                             ) 
            
    def memoryUpdate(self):
        memory = psutil.virtual_memory()        
        self.memory = {'total' : '{:,}'.format(int(memory.total / self.mega)), 
                       'avail' : '{:,}'.format(int(memory.available / self.mega)),
                       'active' : '{:,}'.format(int(memory.active / self.mega)),
                       }    

    
    def update(self):
        self.processUpdate()
        self.cpuUpdate()
        self.memoryUpdate()
        
    def __del__(self):
        pass
        

class MonitorView(TemplateView):        
    
    def get(self, request):
        sysinfo = SyetmeInfomation()                
        sysinfo.update() 
               
        data = { 'processes' : sysinfo.processes,
                 'cpus' : sysinfo.cpus,          
                 'memory' : sysinfo.memory,              
                 }
        
        sysinfo.__del__()
        
        return render(request, 'monitor/index.html', data)    
    
class ProcessView(TemplateView):
    
    def get(self, request, pid):
        proc = psutil.Process(int(pid))        
        output = {'name'    : proc.name(),
                  'pid'     : proc.pid,
                  'ppid'    : proc.ppid(),
                  'exe'     : proc.exe(),
                  'cmdline' : proc.cmdline(),
                  'created' : datetime.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                  'status'  : proc.status(),
                  'cwd'     : proc.cwd(),
                  'username': proc.username(),
                  'uids'    : proc.uids(),
                  'gids'    : proc.gids(),
                  'nice'    : proc.nice(),
                  'ionice'  : proc.ionice(),
                  'rlimit'  : proc.rlimit(psutil.RLIMIT_FSIZE),
                  'io_counters' : proc.io_counters(),
                  'num_ctx_switches' : proc.num_ctx_switches(),
                  'num_fds' : proc.num_fds(),
                  'num_threads' : proc.num_threads(),
                  'threads' : proc.threads(),                  
                  'cpu_times' : proc.cpu_times(),
#                   'cpu_percent' : proc.cpu_percent(),
                  'cpu_affinity' : proc.cpu_affinity(),
                  'memory_info_ex' : proc.memory_info_ex(),
                  'memory_percent' : proc.memory_percent(),
                  'children' : proc.children(),              
                  'open_files' : proc.open_files(),     
                  'connections' : proc.connections(),
                  'is_running' : proc.is_running(),             
                  
                  }
        return render(request, 'monitor/process.html', output)
