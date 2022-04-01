from tkinter import *

ws = Tk()
ws.geometry('700x550')
ws.title('PythonGuides')
ws['bg']='#5d8a82'

f = ("Times bold", 14)

def nextPage():
    ws.destroy()
    import page2

def prevPage():
    ws.destroy()
    import page3
    
Label(
    ws,
    text="Welcome to your remote gait lab",
    padx=20,
    pady=20,
    bg='#5d8a82',
    font=f
).pack(expand=True, fill=BOTH)

## show nothing if nothing available yet
Button(
    ws, 
    text="View weekly summary", 
    font=f,
    command=nextPage
    ).pack(fill=X, expand=TRUE, side=LEFT)

Button(
    ws, 
    text="View Live Plot", 
    font=f,
    command=prevPage
    ).pack(fill=X, expand=TRUE, side=LEFT)

ws.mainloop()