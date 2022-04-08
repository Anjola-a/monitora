
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import itertools 
curr_time = datetime.now().time()
global day  ## fix later
day_f = open('day.csv','r')
day = float(day_f.readlines()[0])
day_f.close()
# prfloat(day)
# if curr_time.hour > 24 and curr_time.minute < 60:
def comp_daily_average():
    global day
    # get daily average and write to file
    if curr_time.hour < 24 and curr_time.minute < 60:
        ##get average and sotre in daily average
        ##read in all the points for the day
        file1 = open('daily_data.csv', 'r')
        Lines = file1.readlines()

        total1 =0
        total2 = 0
        total3 = 0
        cnt = 0
        for line in Lines:
            dataArray = line.split(",")
            cnt += 1
            size = len(dataArray[3])
            dataArray[3] = dataArray[3][:size - 1]
            # prfloat(dataArray)
            total1 += float(dataArray[1])
            total2 += float(dataArray[2])
            total3 += float(dataArray[3])
        day1 = float(total1/cnt)
        day2 = float(total2/cnt)
        day3 = float(total3/cnt)
        # daily_average = (total1/cnt)
        f_average = open('daily_average.csv','a')
        f_average.write(str(day) + "," + str(day1) + "\n")
        f_average.close()
        f_average = open('daily_average2.csv','a')
        f_average.write(str(day) + "," + str(day2) + "\n")
        f_average.close()
        f_average = open('daily_average3.csv','a')
        f_average.write(str(day) + "," + str(day3) + "\n")
        f_average.close()
        day += 1
        f = open('day.csv','w')
        open('daily_data.csv', 'w').close()
        f.write(str(day))
        f.close()
        total1 = 0
        total2 = 0
        total3 = 0
        cnt = 0


# 

# ## weekly report
# ## in the gui if you click weekly is should show you a plot of the data you have so far
# ## maximum of last 5 days
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
    # prfloat("before loops")
    
    for (l1,l2,l3) in zip(f1, f2, f3):
        arr1 = l1.split(',')
        arr2 = l2.split(',')
        arr3 = l3.split(',')
        # prfloat(arr1)
        size = len(arr1[1])
        arr1[1] = arr1[1][:size - 1]
        arr2[1] = arr2[1][:size - 1]
        arr3[1] = arr3[1][:size - 1]
        x_axis.append(float(arr1[0]))
        FSR1.append(float(arr1[1]))
        FSR2.append(float(arr2[1]))
        FSR3.append(float(arr3[1]))
   
    # prfloat(FSR2)
    # prfloat(FSR3)
    # prfloat(FSR1)
    avg_text = ""
    if len(FSR1) > 1:
        diff = FSR1[-1] - FSR1[0]
    # diff2 = FSR1[-2] - FSR1[0]
        if diff > 0:
            avg_text = "There has been an improvement in the GRF generated by the heel strike"
            if FSR1[-1] > 4:
                avg_text = "GRF due to Heel strike has singnificantly improved"
        else:
            # prfloat(diff)
            # prfloat(diff2)
            avg_text = "No substantial improvement in GRF due to heel strike has been observed"
    # Set position of bar on X axis
    br1 = np.arange(len(FSR1))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    
    # Make the plot
    plt.bar(br1, FSR1, color ='r', width = barWidth,
            edgecolor ='grey', label ='Heel')
    plt.bar(br2, FSR2, color ='g', width = barWidth,
            edgecolor ='grey', label ='MT1')
    plt.bar(br3, FSR3, color ='b', width = barWidth,
            edgecolor ='grey', label ='MT2')
    
    # Adding Xticks
    plt.xlabel('Day', fontweight ='bold', fontsize = 15)
    plt.ylabel('Average Force Reading', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(FSR2))],
            x_axis)
    
    plt.legend( loc='upper left')
    
    plt.savefig('average.png')
    # plt.show()
    plt.close()
    return(avg_text)

# comp_daily_average()
# prfloat(plot_average())