from time import perf_counter as time
import subprocess
import psutil
import sys
import threading 
import numpy as np
from functools import wraps

def collectUtil(fn):
    @wraps(fn)
    def measure(*args, **kwargs):
        def collect(event, args):
                f=open("test.dat", "w")
                measurements=np.array([0]*psutil.cpu_count())
                for i in measurements:
                    f.write(str(i) + " ")
                f.write(f"{time()} \n")
                while not event.is_set():
                    perc=psutil.cpu_percent(interval=0.25, percpu=True)
                    for i in perc:
                        f.write(str(i) + " ")
                    f.write(f"{time()} \n")
                f.close()
                return
        stopEvent=threading.Event()
        t=threading.Thread(target=collect, args=(stopEvent, False))
        t.start()
        result=fn(*args, **kwargs)
        stopEvent.set()
        t.join()
        subprocess.Popen([sys.executable, "PlotCPU.py", "test.dat"])
        return result
    return measure

