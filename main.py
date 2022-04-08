import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from averager import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import serial as sr
import time
from datetime import datetime

f = ("Times bold", 14)
root = tk.Tk()
root.title('Remote gait lab')
root.geometry("994x576")
root.configure(bg = "#ffffff")


# ---- functions ----------

# frame function shows the frame to the screen
def show_frame(frame):
    frame.tkraise()

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
temp1 = 1
c = 0
r = 0
# home page functions --------
def plot_data():
    # print("here1")
    global cond, data, ms,FSRreading,gait_t,GFR_range,cnt, x_s, x_end,s,temp1,c,r
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
       
        if not a:
           print("nothing to read")
        
        if(len(GFR_range) < 45 and t < 15):
            
            GFR_range.append(int(dataArray[0]))
            gait_t.append(t)
        else:
            if temp1 == 1:
                c = len(GFR_range)
                r = gait_t[0]
                temp1 = 2
            GFR_range[0:c-1] = GFR_range[1:c]
            GFR_range[c-1] = int(dataArray[0])
            gait_t[0:c-1] = gait_t[1:c]
            gait_t[c-1] = t
            x_s = t-13+r
            x_end = t+0.5
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
    
s = ""
varr2 = 0
def plot_start():
    global cond, ms, cnt, s,varr2
    if cnt == 0:  
        ms = time.time()
        cnt = 1
        if varr2 == 0:
        #----start serial port----
            s = sr.Serial('COM3',115200);
            s.reset_input_buffer()
            varr2 = 1
    cond = True
    s.reset_input_buffer()

def plot_stop():
    global cond,FSRreading,gait_t
    cond = False
    # FSRreading = []
    # gait_t = []
    # ms = time.time()

def exit_plot():
    global cnt, FSRreading, GFR_range, cond, gait_t,x_s, x_end,temp1
    cnt = 0
    FSRreading = []
    GFR_range = []
    temp1 = 1
    gait_t = []
    x_s = 0
    x_end =15
    ax.set_xlim(x_s,x_end)
    cond = False
    comp_daily_average()

img_avg = Image.open("average.png")
result = ""
def generate_plot():
    ##left mt1
    global img_avg, result
    # print(" in plot herreee")
    # comp_daily_average()
    result = plot_average()
    img_avg = Image.open("average.png")
    img_avg = img_avg.resize((750, 400), Image.ANTIALIAS)
    img_avg = ImageTk.PhotoImage(img_avg)
    label_avg_img = Label(overview, image=img_avg)
    label_avg_img.image = img_avg
    label_avg_img.place(x=145, y=110)
    text = Label(overview, text=result, font=("Helvetica", 19))
    text.place(x=148,y=519)
    show_frame(overview)
    
# --- creating/initializing all of our frames ---
home = tk.Frame(root)
live_plot = tk.Frame(root)
overview = tk.Frame(root)

for frame in (home, live_plot, overview):
    frame.grid(row=0, column=0, sticky='nsew')
# setting the first frame that you see ---

# setting the first frame that you see ---
# show_frame(live_plot)

# -------- setting up home page ------------
# --- background fir live plot image --
background_img0 = PhotoImage(file=f"home_bkgd.png")
frame0_title = tk.Label(home, image=background_img0)
frame0_title.pack(fill='x')

home_var = True
def set_home():
    global home_var
    home_var = not home_var
# -- buttons --

img_btn_lvp = PhotoImage(file=f"liveplt_btn.png")
img_btn_avg = PhotoImage(file=f"avg_btn.png")


btn_lvp = Button(home, image=img_btn_lvp, borderwidth=0, highlightthickness=0,
            command=lambda: [set_home(), show_frame(live_plot)], relief="flat")
btn_lvp.place(x = 796, y = 228, width = 161, height = 93)

btn_avg = Button(home, image=img_btn_avg
, borderwidth=0, highlightthickness=0,
            command=lambda: [set_home(), generate_plot()], relief="flat")
btn_avg.place(x = 796, y = 388, width = 161, height = 93)

## fix issue with old plot


# -------- setting up weekly average page ------------
# --- background for live plot image --
background_img1 = PhotoImage(file=f"avg_bkgd.png")
frame2_title = tk.Label(overview, text="this is frame one", image=background_img1)
frame2_title.pack(fill='x')


img_hm_btn = PhotoImage(file=f"hm_btn.png")

hm_btn = Button(overview, image=img_hm_btn
, borderwidth=0, highlightthickness=0,
            command=lambda: [set_home(), show_frame(home)], relief="flat")
hm_btn.place(x = 839, y = 58, width = 138, height = 39)

# img_avg = img_avg.resize((750, 400), Image.ANTIALIAS)
# img_avg = ImageTk.PhotoImage(img_avg)
# label_avg_img = Label(overview, image=img_avg)
# label_avg_img.image = img_avg
# label_avg_img.place(x=145, y=110)

# text = Label(overview, text=" ", font=("Helvetica", 19))
# text.place(x=247,y=540)

# -------- setting up live plot ------------
# add figure canvas
fig = Figure();
ax = fig.add_subplot(111)

#ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax.set_title('GRF range Data for heel');
ax.set_xlabel('time')
ax.set_ylabel('FSR range for heel')
ax.set_xlim(x_s,x_end)
ax.set_ylim(0,8.3)
ax.grid(True)
lines = ax.plot([],[])[0]



# --- background for live plot image --
background_img = PhotoImage(file=f"liveplot_bkgd.png")
frame1_title = tk.Label(live_plot, text="this is frame one", image=background_img)
frame1_title.pack(fill='x')

canvas = FigureCanvasTkAgg(fig, master=live_plot)  # A tk.DrawingArea. want to display in root window
canvas.get_tk_widget().place(x = 161.92, y=111.08, width = 620.63,height = 405.1)
canvas.draw()
# -- buttons --

img0 = PhotoImage(file=f"start_btn.png")
img1 = PhotoImage(file=f"stop_btn.png")
img3 = PhotoImage(file=f"home_btn.png")

start = Button(live_plot, image=img0, borderwidth=0, highlightthickness=0,
            command=plot_start, relief="flat")
start.place(x = 815, y = 139, width = 148, height = 43)

stop = Button(live_plot, image=img1, borderwidth=0, highlightthickness=0,
            command=plot_stop, relief="flat")
stop.place(x = 815, y = 293, width = 148, height = 43)

homebtn = Button(live_plot, image=img3, borderwidth=0, highlightthickness=0,
            command=lambda: [set_home(), exit_plot(), show_frame(home)], relief="flat")
homebtn.place(x = 815, y = 447, width = 148, height = 43)

if home_var:
    show_frame(home)
root.after(1,plot_data)
root.mainloop()
