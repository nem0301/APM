from django.shortcuts import render
from models import Monitor
from django.views.generic.base import TemplateView
import threading, datetime
from SystemInformation import SystemInformation 
sysInfo = SystemInformation()

th = threading.Thread(target=sysInfo.loopThread, args=(1,))
th.start()
        
class MonitorView(TemplateView):        
    def get(self, request):
        global sysInfo
        sysinfo = sysInfo
        data = {'processes' : sysinfo.allProcesses,
                'processesByCpu' : sysinfo.processesByCpu,
                'processesByMemory' : sysinfo.processesByMemory,
                'cpus' : sysinfo.cpus,          
                'memory' : sysinfo.memory,
                'refreshInterval': 1000,              
                 }
        
        sysinfo.__del__()
        
        return render(request, 'monitor/overall.html', data)    
    
class ProcessView(TemplateView):
    
    def get(self, request, pid):
        global sysInfo        
        proc = sysInfo.getProcessByPid(pid)
        if (proc == False):
            print ("There is no Process with the pid : %d" % int(pid))
        parentName = "None"
        
        #This process is first process after system boot. There is No parent process
        if int(proc.ppid()) != 0:
            parentProcess = sysInfo.getProcessByPid(int(proc.ppid()))
            parentName = parentProcess.name()
                    
        memory_info_ex = proc.memory_info_ex()        
        memory_info =  {'rss' : '{:,}'.format(memory_info_ex.rss),
                        'vms' : '{:,}'.format(memory_info_ex.vms),
                        'shared' : '{:,}'.format(memory_info_ex.shared),
                        'text' : '{:,}'.format(memory_info_ex.text),
                        'lib' : '{:,}'.format(memory_info_ex.lib),
                        'data' : '{:,}'.format(memory_info_ex.data),
                        'dirty' : '{:,}'.format(memory_info_ex.dirty),
                        }
        
        
        output = {'name'    : proc.name(),
                  'pid'     : proc.pid,
                  'parent_name' : parentName,
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
                  'io_counters' : proc.io_counters(),
                  'num_ctx_switches' : proc.num_ctx_switches(),
                  'num_fds' : proc.num_fds(),
                  'num_threads' : proc.num_threads(),
                  'threads' : proc.threads(),                  
                  'cpu_times' : proc.cpu_times(),
                  'cpu_percent' : proc.cpu_percent(),
                  'cpu_affinity' : proc.cpu_affinity(),
                  'memory_info_ex' : memory_info,
                  'memory_percent' : proc.memory_percent(),
                  'children' : proc.children(),              
                  'open_files' : proc.open_files(),     
                  'connections' : proc.connections(),
                  'is_running' : proc.is_running(), 
                  'refreshInterval' : 1000,            
                  
                  }
        return render(request, 'monitor/process.html', output)




