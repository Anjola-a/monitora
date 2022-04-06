from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import serial as sr
import time
from datetime import datetime

root = tk.Tk()
root.title('Real time Plot')
root.configure(background= "light blue")
root.geometry('700x500')  ## sets window size
from tkinter import *

#------global variables
data = np.array([])
cond = False
FSRreading = []
GFR_range = []
gait_t = []
ms = 0
x_s = 0
x_end = 15
cnt = 0
#-----plot data-----
def plot_data():
    # print("here1")
    global cond, data, ms,FSRreading,gait_t,GFR_range,cnt, x_s, x_end
    if (cond == True):
        
        a = s.readline()
        arduinoString = a.decode()
        dataArray = arduinoString.split(',')
        size = len(dataArray[2])
        dataArray[2] = dataArray[2][:size - 2]
        ct = time.time()
        t = (ct-ms)
        print(dataArray)
        FSRreading.append(int(dataArray[1]))
       
        
        if(len(GFR_range) < 46):
            GFR_range.append(int(dataArray[0]))
            gait_t.append(t)
        else:
            GFR_range[0:45] = GFR_range[1:46]
            GFR_range[45] = int(dataArray[0])
            gait_t[0:45] = gait_t[1:46]
            gait_t[45] = t
            # x_s += 0.31
            # x_end += 0.27
            x_s = t-13
            x_end = t
            ax.set_xlim(x_s,x_end)
            
		# print(gait_t)
        lines.set_xdata(gait_t)
        lines.set_ydata(GFR_range)
        
        print(gait_t)
    
        ## gets wiped everyday
        f = open('daily_data.csv','a')
        f.write(str(t) + "," + dataArray[0] + "," + dataArray[1] + "," + dataArray[2] + '\n')
        f.close()

        f = open('all_data.csv','a')
        f.write(str(t) + "," + dataArray[0] + "," + dataArray[1] + "," + dataArray[2] + '\n')
        f.close()
        
        
        canvas.draw()
    root.after(1,plot_data)
    
    
    

def plot_start():
    global cond, ms, cnt
    if cnt == 0:
        ms = time.time()
        cnt = 1
    cond = True
    s.reset_input_buffer()

def plot_stop():
    global cond
    cond = False
#------create Plot object on GUI----------
# add figure canvas
fig = Figure();
ax = fig.add_subplot(111)

#ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax.set_title('GRF range Data');
ax.set_xlabel('time')
ax.set_ylabel('FSR range')
ax.set_xlim(x_s,x_end)
ax.set_ylim(0,9)
ax.grid(True)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea. want to display in root window
canvas.get_tk_widget().place(x = 122,y=65, width = 500,height = 400)
canvas.draw()

#----------create button---------
root.update();
start = tk.Button(root, text = "Start", font = ('calbiri',12),command = lambda: plot_start())
start.place(x = 100, y = 450 )

root.update();

def prevPage():
    root.destroy()
    import page1
    # import demo_analysis
    
stop = tk.Button(root, text = "Stop", font = ('calbiri',12), command = lambda:plot_stop())
back = tk.Button(root, text = "HomePage", font = ('calbiri',12), command = lambda:prevPage())
back.place(x = start.winfo_x()+start.winfo_reqwidth() + 100, y = 450)
stop.place(x = start.winfo_x()+start.winfo_reqwidth() + 20, y = 450)

#----start serial port----
s = sr.Serial('COM8',115200);
s.reset_input_buffer()

# --- creating/initializing all of our frames ---
home = tk.Frame(root)
exercise_one = tk.Frame(root)
exercise_two = tk.Frame(root)
result = tk.Frame(root)
    
root.after(1,plot_data)
root.mainloop()



## I'll adjust accel values based on 3d print stuff