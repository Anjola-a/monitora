from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("994x576")
window.configure(bg = "#f6e9ff")
canvas = Canvas(
    window,
    bg = "#f6e9ff",
    height = 576,
    width = 994,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 355, y = 168,
    width = 138,
    height = 39)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    0.0, -12.0,
    image=background_img)

window.resizable(False, False)
window.mainloop()
