import tkinter as tk
from os.path import dirname

class Cell(tk.Label):
    def __init__(self,master,pos):
        tk.Label.__init__(self,master)
        self.off()
        self.bind('<Button-1>',self.swithState)
        self.config(border=0)
        self.grid(column=pos[0],row=pos[1],pady=1,padx=1)
    def on(self):
        self.status=True
        self.config(bitmap='@'+dirname(__file__)+'/1.xbm')
    def off(self):
        self.status=False
        self.config(bitmap='@'+dirname(__file__)+'/0.xbm')
    def swithState(self,event):
        if self.status:
            self.off()
        else:
            self.on()

class GameGrid(tk.Frame):
    def __init__(self,master,size):
        tk.Frame.__init__(self,master,border=1,background='black')
        self.grid()
        self.columns=[]
        self.rows=[]
        for y in range(size[1]):
            for x in range(size[0]):
                Cell(self,(x,y))
        
class App(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.geometry('400x250')
        self.master.title('Griddler')
        GameGrid(self,(15,10)).grid(sticky='W')

App().mainloop()
