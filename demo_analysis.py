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
       
        
        if(len(GFR_range) < 30):
            GFR_range.append(int(dataArray[2]))
            gait_t.append(t)
        else:
            GFR_range[0:29] = GFR_range[1:30]
            GFR_range[29] = int(dataArray[2])
            gait_t[0:29] = gait_t[1:30]
            gait_t[29] = t
            x_s += 0.5
            x_end += 0.5
            ax.set_xlim(x_s,x_end)
            
		
        lines.set_xdata(gait_t)
        lines.set_ydata(GFR_range)
        
        # print(gait_t)
    
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
    global cond, ms
    ms = time.time()
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
ax.set_ylim(0,6)
ax.grid(True)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea. want to display in root window
canvas.get_tk_widget().place(x = 10,y=10, width = 500,height = 400)
canvas.draw()

#----------create button---------
root.update();
start = tk.Button(root, text = "Start", font = ('calbiri',12),command = lambda: plot_start())
start.place(x = 100, y = 450 )

root.update();
stop = tk.Button(root, text = "Stop", font = ('calbiri',12), command = lambda:plot_stop())
stop.place(x = start.winfo_x()+start.winfo_reqwidth() + 20, y = 450)

#----start serial port----
s = sr.Serial('COM8',115200);
s.reset_input_buffer()

root.after(1,plot_data)
root.mainloop()



## I'll adjust accel values based on 3d print stuff