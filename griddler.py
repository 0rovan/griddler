"""
griddler - not sure yet
Copyright (C) 2015 0rovan

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import tkinter as tk
from os.path import dirname


class Hint(tk.Frame):
    def __init__(self,master,pos):
        tk.Frame.__init__(self,master,background='black')
        self.pos=pos
        glue='E' if pos[1] else 'S'
        self.grid(column=pos[0],row=pos[1],sticky=glue)
        self.cells=[]
        tk.Label(self,text='0',font='Mono 9',width=2).grid(padx=1,pady=1)
    def recount(self):
        values=[]
        count=0
        for cell in self.cells:
            if cell.status:
                count+=1
            elif count:
                values.append(count)
                count=0
        if count:
            values.append(count)
        if not values:
            values=[0]
        for child in self.winfo_children():
            child.destroy()
        count=0
        for value in values:
            if self.pos[1]:
                x=count
                y=0
                padx=1
                pady=0
            else:
                x=0
                y=count
                padx=0
                pady=1
            tk.Label(self,text=str(value),font='Mono 9',width=2).grid(column=x,row=y,pady=pady,padx=padx)
            count+=1


class Cell(tk.Label):
    def __init__(self,master,hints):
        tk.Label.__init__(self,master)
        self.hints=hints
        for hint in hints:
            hint.cells.append(self)
        self.off()
        self.bind('<Button-1>',self.swithState)
        self.config(border=0)
        self.grid(column=hints[0].pos[0],row=hints[1].pos[1],pady=1,padx=1)
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
        for hint in self.hints:
            hint.recount()

class GameGrid(tk.Frame):
    def __init__(self,master,size):
        tk.Frame.__init__(self,master,border=1,background='black')
        self.grid()
        self.columns=[]
        self.rows=[]
        for x in range(size[0]):
            self.rows.append(Hint(self,(x+1,0)))
        for y in range(size[1]):
            column=Hint(self,(0,y+1))
            for x in range(size[0]):
                Cell(self,(self.rows[x],column))
        
class App(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.geometry('500x350')
        self.master.title('Griddler')
        GameGrid(self,(15,10)).grid(sticky='W')

App().mainloop()
