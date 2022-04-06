import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import global_var
import global_func
import data_analysis
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

window = tk.Tk()
f = ("Times bold", 14)


# ---- functions ----------

# frame function shows the frame to the screen
def show_frame(frame):
    frame.tkraise()

# main page functions
def set_exercise_one_off():
    global_var.exercise_one = False

def set_exercise_one_on():
    global_var.exercise_one = True

# exercise_one functions --------
def plot_data():
    global condition
    global data

    if condition:
        arduinoString = global_func.arduinoData.readline()
        data_array = arduinoString.decode().split(',')  # split on comma

        # keeps only 100 data points
        if len(data) < 50:
            data = np.append(data, float(data_array[0]))
        else:
            data[0:49] = data[1:50]
            data[49] = float(data_array[0])

        global_var.euler_data.append(float(data_array[0]))
        # force data
        global_var.force_data.append(float(data_array[1]))

        if global_var.exercise_one:
            lines_1.set_xdata(np.arange(start=0, stop=len(data), step=1))
            lines_1.set_ydata(data)
        else:
            lines_2.set_xdata(np.arange(start=0, stop=len(data), step=1))
            lines_2.set_ydata(data)

        if global_var.exercise_one:
            canvas_one.draw()
        else:
            canvas_two.draw()

    global AFTER
    AFTER = window.after(1, plot_data)


def plot_start():
    global condition
    global_var.data_on()
    condition = True
    global_func.arduinoData.reset_input_buffer()


def plot_end():
    global condition
    global data
    condition = False
    data_analysis.rom_analysis()


def reset_data():
    global data
    data = []

# --- updating result page functions ---
def change_data_text():
    global rom_label
    global force_label
    global label_force_img
    global label_angle_img
    global word_label

    print("changing ROM")
    rom_label.configure(text=global_var.rom_value_text)
    force_label.configure(text=global_var.force_value_text)
    word_label.configure(text=global_var.rom_phrase)

    img_force = Image.open("force.png")
    img_force = img_force.resize((250, 250), Image.ANTIALIAS)
    img_force = ImageTk.PhotoImage(img_force)
    label_force_img.configure(image = img_force)
    label_force_img.image = img_force


    if global_var.exercise_one:
        img = Image.open("euler_reverse.png")
    else:
        img = Image.open("euler_rotation.png")

    img_angle = img.resize((250, 250), Image.ANTIALIAS)
    img_angle = ImageTk.PhotoImage(img_angle)
    label_angle_img.configure(image=img_angle)
    label_angle_img.image = img_angle

# function i'm not sure I need rn
# def callback():
#     global after_id
#     var.set(var.get() + 1)
#     after_id = window.after(500, callback)
#     # print('in callback function')
#     window.protocol('WM_DELETE_WINDOW', quit)


# make sures that the window will expand

# -------- creating the window ------
window.geometry("792x612")
window.configure(bg="#ffffff")

# --- creating/initializing all of our frames ---
home = tk.Frame(window)
exercise_one = tk.Frame(window)
exercise_two = tk.Frame(window)
result = tk.Frame(window)

for frame in (home, exercise_one, exercise_two, result):
    frame.grid(row=0, column=0, sticky='nsew')

# setting the first frame that you see ---
show_frame(home)

# -------- setting up home page ------------

# --- background image --
background_img = ImageTk.PhotoImage(Image.open("main_bkgd.png"))
frame1_title = tk.Label(home, text="this is frame one", image=background_img)
frame1_title.pack(fill='x')

# -- buttons --

img0 = PhotoImage(file=f"reverse_fly_btn.png")
img1 = PhotoImage(file=f"side_lying_btn.png")

b0 = Button(home, image=img0, borderwidth=0, highlightthickness=0,
            command=lambda: [set_exercise_one_on(),show_frame(exercise_one)], relief="flat")
b0.place(x=329, y=422, width=200, height=76)

b1 = Button(home, image=img1, borderwidth=0, highlightthickness=0,
            command=lambda: [set_exercise_one_off(),show_frame(exercise_two)], relief="flat")
b1.place(x=561, y=422, width=200, height=76)

# ----------- exercise one -------------
data = np.array([])
condition = False

background_img_e1 = PhotoImage(file=f"reverse_fly_bkgd.png")
frame1_title = tk.Label(exercise_one, text="this is frame one", image=background_img_e1, bg='white')
frame1_title.place(x=0, y=0)

# buttons
start_btn = PhotoImage(file=f"start_btn.png")
end_btn = PhotoImage(file=f"end_btn.png")
results_btn = PhotoImage(file=f"results_btn.png")

b0 = Button(exercise_one, image=start_btn, borderwidth=0, highlightthickness=0, command=plot_start, relief="flat")
b0.place(x=526, y=20, width=200, height=76)

b1 = Button(exercise_one, image=end_btn, borderwidth=0, highlightthickness=0, command=plot_end, relief="flat")
b1.place(x=526, y=105, width=200, height=76)

b2 = Button(exercise_one, image=results_btn, borderwidth=0, highlightthickness=0, command=lambda: [change_data_text(), show_frame(result)],
            relief="flat")
b2.place(x=526, y=190, width=200, height=76)

# adding in graph
fig_1 = Figure()
ax_1 = fig_1.add_subplot(111)

ax_1.set_title('Degrees vs. # of Data Points')
ax_1.set_ylabel('Degrees')
ax_1.set_ylim(-180, 360)
ax_1.set_xlim(0, 50)
lines_1 = ax_1.plot([], [])[0]  # this gives an array that is varying moved as global variable

canvas_one = FigureCanvasTkAgg(fig_1, master=exercise_one)  # A tk.DrawingArea
canvas_one.get_tk_widget().place(x=475, y=270, width=300, height=325)
canvas_one.draw()

# ------- exercise two page -------
data = np.array([])
condition = False

background_img_e2 = PhotoImage(file=f"side-lying_bkgd.png")
frame2_title = tk.Label(exercise_two, text="this is exercise two", image=background_img_e2, bg='white')
frame2_title.place(x=0, y=0)

# buttons
start_btn_2 = PhotoImage(file=f"start_btn.png")
end_btn_2 = PhotoImage(file=f"end_btn.png")
results_btn_2 = PhotoImage(file=f"results_btn.png")

btn_start = Button(exercise_two, image=start_btn_2, borderwidth=0, highlightthickness=0, command=plot_start, relief="flat")
btn_start.place(x=526, y=20, width=200, height=76)

btn_end = Button(exercise_two, image=end_btn_2, borderwidth=0, highlightthickness=0, command=plot_end, relief="flat")
btn_end.place(x=526, y=105, width=200, height=76)

btn_results = Button(exercise_two, image=results_btn_2, borderwidth=0, highlightthickness=0, command=lambda: [change_data_text(), show_frame(result)],
            relief="flat")
btn_results.place(x=526, y=190, width=200, height=76)

# adding in graph
fig_2 = Figure()
ax_2 = fig_2.add_subplot(111)

ax_2.set_title('Degrees vs. # of Data Points')
ax_2.set_ylabel('Degrees')
ax_2.set_ylim(-180, 360)
ax_2.set_xlim(0, 50)
lines_2 = ax_2.plot([], [])[0]  # this gives an array that is varying moved as global variable

canvas_two = FigureCanvasTkAgg(fig_2, master=exercise_two)  # A tk.DrawingArea
canvas_two.get_tk_widget().place(x=475, y=270, width=300, height=325)
canvas_two.draw()

# --------- Result page -----------
background_img_results = PhotoImage(file=f"results_bkgd.png")
frame1_title = tk.Label(result, text="this is frame one", image=background_img_results, bg='white')
frame1_title.place(x=0, y=0)

home_btn = PhotoImage(file=f"home_btn.png")
h_btn = Button(result, image=home_btn, borderwidth=0, highlightthickness=0,
               command=lambda: [reset_data(), show_frame(home)], relief="flat")
h_btn.place(x=666, y=8, width=175, height=44)

if global_var.exercise_one:
    img_results = Image.open("euler_reverse.png")
elif global_var.exercise_one == False:
    img_results = Image.open("euler_rotation.png")

# loading in graphs for results for angles and force
global label_angle_img
global label_force_img

img = img_results.resize((250, 250), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
label_angle_img = Label(result, image=img)
label_angle_img.image = img
label_angle_img.place(x=26, y=299)


img_force = Image.open("force.png")
img_force = img_force.resize((250, 250), Image.ANTIALIAS)
img_force = ImageTk.PhotoImage(img_force)
label_force_img = Label(result, image=img_force)
label_force_img.image = img_force
label_force_img.place(x=515, y=299)

# loading in the ROM value text and force values
global rom_label
rom_label = Label(result, text=global_var.rom_value_text, font=f,
      bg='#FDF6EC')
rom_label.place(x=375, y=195)

global force_label
force_label = Label(result, text=global_var.force_value_text, font=f,
      bg='#FDF6EC')
force_label.place(x=375, y=285)

global word_label
word_label= Label(result, text=global_var.rom_phrase, font=f, bg='#FDF6EC')
word_label.place(x=295, y = 380)


window.after(1, plot_data)
print("looping")
window.mainloop()