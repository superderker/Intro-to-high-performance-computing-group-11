import matplotlib.pyplot as plt
import numpy as np
import sys
def doPlot(filename):
    data=np.loadtxt(filename)
    shape=np.shape(data)
    startval=data[:,-1][0]
    data[:,-1]=data[:,-1]-startval
    print("\nCore usage in percentage")
    for i in range(shape[1]-1):
        string="Core " + str(i+1)
        print(f"{string:<11}", end='', flush=True)
    timeStr="time"
    print(f"{timeStr:<11}")

    def mapFunc(val):
        return f"{val:<10.5}"
    for i in range(shape[0]):
        res=map(mapFunc, data[i,:])
        print(*res)
    plt.figure(figsize=(10,6))
    for i in range(shape[1]-1):
        plt.plot(data[:,-1],data[:,i], label=f"Core {i+1}")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid()
    plt.axis([None, None, 0, 100])
    plt.show()


   

if __name__ == "__main__":
    doPlot(sys.argv[1])