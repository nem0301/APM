import psutil, time

class SystemInformation:
    
    kilo = 1024
    mega = kilo * kilo
    giga = mega * kilo  
    
    def __init__(self):
        self.name = 'test'
        self.allProcesses = []
        self.processesByMemory = []
        self.processesByCpu = []
        self.cpus = []
        self.memory = {}
        
    def byName(self, item):
        return item['name']
    
    def byPID(self, item):
        return item['pid']            
        
    def byCpu(self, item):
        return item['cpu_percent']
    
    def byRam(self, item):
        return item['mem_percent']
        
    def getName(self):
        return self.name
    
    def getProcessByPid(self, pid):
        for proc in psutil.process_iter():
            if int(proc.pid) == int(pid):             
                return proc
        return False 
    
    def processUpdate(self):
        pInfo = []
        for proc in psutil.process_iter():            
            memory = {'rss' : '{:,}'.format(proc.memory_info().rss),
                      'vms' : '{:,}'.format(proc.memory_info().vms),
                      'rssM' : '{:,}'.format(proc.memory_info().rss / self.mega),
                      'vmsM' : '{:,}'.format(proc.memory_info().vms / self.mega),
                      }
            proc = {'name' : proc.name(),
                    'pid' : proc.pid, 
                    'cpu_percent' : proc.cpu_percent(), 
                    'memory' : memory,              
                    'mem_percent' : "%05.2f" % proc.memory_percent(),
                    }                   
            pInfo.append(proc)
                    
        
        pInfo.sort(key=self.byName, reverse=False)
        pInfo.sort(key=self.byPID, reverse=True)                        
        self.allProcesses = pInfo[:]
        
        pInfo.sort(key=self.byCpu, reverse=True)
        self.processesByCpu = pInfo[:]
        self.processesByCpu = self.processesByCpu[:5]
        
        pInfo.sort(key=self.byRam, reverse=True)
        self.processesByMemory = pInfo[:] 
        self.processesByMemory = self.processesByMemory[:5]         
        
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
        
    def networkUpdate(self):
        pass    

    
    def update(self):
        self.processUpdate()
        self.cpuUpdate()
        self.memoryUpdate()
        
    def loopThread(self, interval=1):
        while True:
            self.update()
            time.sleep(interval)
        
    def __del__(self):
        pass
    

 