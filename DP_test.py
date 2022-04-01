import serial # import serial library
import numpy
import matplotlib.pyplot as plt
from drawnow import *
import time
from datetime import datetime
arduinoData = serial.Serial('COM8', 115200)
# arduinoData = serial.Serial(115200)
FSRreading = []
GFR_range = []
gait_t = []
plt.ion() # tell matplotlib you eant interactive mode to plot live data
cnt=0
counter = 0
total = 0
ms = time.time()
def makeFig(): #create a fucntion that makes our desired plot
    plt.ylim(1,10) #set limite of first y axis
    plt.title("My life streaming sensor data")
    plt.grid(True)
    plt.ylabel("GFR range")
    plt.plot(gait_t, GFR_range, 'ro-', label='GFR range')
    plt.legend(loc='upper left')

    #--- plotting two things on a plot ------
    # plt2=plt.twinx()
    # plt.ylim(200,1000)  #Set limits of second y axis
    # plt2.plot(FSRreading, "b^-", label='Toe GFR range')
    # plt2.ticklabel_format(useOffset=False)  ## Force matplotlib not to autoscale y axis
    # plt2.legend(loc='upper right')

'''
Plot incoming live data as well as write to file for the day
## plot vs time
'''

while True: #infinite loop
    while (arduinoData.inWaiting() == 0): ## Wait here untill there is data
        pass # do nothing
    arduinoString = arduinoData.readline().decode("utf-8") 
    print(arduinoString)
    # print("here")
    dataArray = arduinoString.split(',')
    # print(dataArray)
2
    ct = time.time()
    t = (ct-ms)
    gait_t.append(t)
    GFR_range.append(int(dataArray[1]))
    # FSRreading.append(int(dataArray[1]))
    print(t)
    
    drawnow(makeFig)  # call drawnow to update our live graph
    plt.pause(0.00001)
    cnt=cnt+1
    
    if(cnt > 30):
        GFR_range.pop(0) ## plotting last 30 points
        gait_t.pop(0)
    ## write time and data to file
    curr_time = datetime.now().time()
    f = open('daily_data.csv','a')
    f.write(str(t) + "," + dataArray[0] + "," + dataArray[1] + '\n')
    


