
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import itertools 
curr_time = datetime.now().time()
global day  ## fix later
day_f = open('day.csv','r')
day = int(day_f.readlines()[0])
day_f.close()
print(day)
# if curr_time.hour > 24 and curr_time.minute < 60:
def comp_daily_average():
    global day
    # print(curr_time.hour)
    # print(curr_time.minute)
    # get daily average and write to file
    if curr_time.hour < 24 and curr_time.minute < 60:
        ##get average and sotre in daily average
        ##read in all the points for the day
        file1 = open('daily_data.csv', 'r')
        Lines = file1.readlines()

        t1 =0
        t2 = 0
        t3 = 0
        cnt = 0
        for line in Lines:
            dataArray = line.split(",")
            cnt += 1
            size = len(dataArray[3])
            dataArray[3] = dataArray[3][:size - 1]
            print(dataArray)
            t1 += int(dataArray[1])
            t2 += int(dataArray[2])
            t3 += int(dataArray[3])
        d1 = int(t1/cnt)
        d2 = int(t2/cnt)
        d3 = int(t3/cnt)
        # daily_average = (t1/cnt)
        f_average = open('daily_average.csv','a')
        f_average.write(str(day) + "," + str(d1) + "\n")
        f_average.close()
        f_average = open('daily_average2.csv','a')
        f_average.write(str(day) + "," + str(d2) + "\n")
        f_average.close()
        f_average = open('daily_average3.csv','a')
        f_average.write(str(day) + "," + str(d2) + "\n")
        f_average.close()
        day += 1
        f = open('day.csv','w')
        open('daily_data.csv', 'w').close()
        f.write(str(day))
        f.close()
        t1 = 0
        t2 = 0
        t3 = 0
        cnt = 0




# ## weekly report
# ## in the gui if you click weekly is should show you a plot of the data you have so far
# ## maximum of last 5 days

def plot_averages():
    avg_overview = plt.figure()
    f_average = open('daily_average.csv','r')
    Lines = f_average.readlines()
    x_axis = []
    height = []
    for (l1, l2, l3) in zip():
        for i in range(3):
            arr = line.split(',')
        # size = len(arr[1])
        # arr[1] = arr[1][:size - 1]
        print(arr[1])
        x_axis.append(int(arr[0]))
        height.append(int(arr[1]))
    # ax = avg_overview.add_axes([0,0,1,1])
    plt.bar(x_axis,height)
    plt.ylabel("GFR range")
    plt.xlabel("Day")
    plt.show()



# comp_daily_average()




def plot_average():
    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))
    
    f1 = open('daily_average.csv','r').readlines()
    f2 = open('daily_average2.csv','r').readlines()
    f3 = open('daily_average3.csv','r').readlines()
    # f1 = f1.readlines()
    x_axis = []
    FSR1 = []
    FSR2 = []
    FSR3 = []
    # print("before loops")
    
    for (l1,l2,l3) in zip(f1, f2, f3):
        arr1 = l1.split(',')
        arr2 = l2.split(',')
        arr3 = l3.split(',')
        size = len(arr1[1])
        arr1[1] = arr1[1][:size - 1]
        arr2[1] = arr2[1][:size - 1]
        arr3[1] = arr3[1][:size - 1]
        x_axis.append(int(arr1[0]))
        FSR1.append(int(arr1[1]))
        FSR2.append(int(arr2[1]))
        FSR3.append(int(arr3[1]))
   
    print(FSR2)
    print(FSR3)
    print(FSR1)
    # Set position of bar on X axis
    br1 = np.arange(len(FSR1))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    
    # Make the plot
    plt.bar(br1, FSR1, color ='r', width = barWidth,
            edgecolor ='grey', label ='FSR1')
    plt.bar(br2, FSR2, color ='g', width = barWidth,
            edgecolor ='grey', label ='FSR2')
    plt.bar(br3, FSR3, color ='b', width = barWidth,
            edgecolor ='grey', label ='FSR3')
    
    # Adding Xticks
    plt.xlabel('Day', fontweight ='bold', fontsize = 15)
    plt.ylabel('Average Force Reading', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(FSR2))],
            x_axis)
    
    plt.legend()
    plt.show()


plot_average()