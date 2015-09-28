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

    def count(self):
        values=[]
        count=0
        for cell in self.cells:
            if cell.status==1:
                count+=1
            elif count:
                values.append(count)
                count=0
        if count:
            values.append(count)
        return values if values else [0]

    def update(self,values):
        for child in self.winfo_children():
            child.destroy()
        pos=0
        for value in values:
            if self.pos[1]:
                x=pos
                y=0
                padx=1
                pady=0
            else:
                x=0
                y=pos
                padx=0
                pady=1
            tk.Label(self,text=str(value),font='Mono 9',width=2).grid(column=x,row=y,pady=pady,padx=padx)
            pos+=1


class Cell(tk.Label):

    def __init__(self,master,hints):
        tk.Label.__init__(self,master)
        self.hints=hints
        for hint in hints:
            hint.cells.append(self)
        self.status=None
        self.swithState(None,0)
        self.bind('<Button-1>',lambda e:self.swithState(e,1))
        self.bind('<Button-3>',lambda e:self.swithState(e,0))
        self.config(border=0)
        self.grid(column=hints[0].pos[0],row=hints[1].pos[1],pady=1,padx=1)


    def swithState(self,event,color=1):
        if color!=self.status:
            self.status=color
            self.config(bitmap='@'+dirname(__file__)+'/'+str(color)+'.xbm')
            for hint in self.hints:
                hint.update(hint.count())


class GameGrid(tk.Frame):

    def __init__(self,master,size):
        tk.Frame.__init__(self,master,border=2,background='black',relief='sunken')
        self.grid()
        self.columns=[]
        self.rows=[]
        for x in range(size[0]):
            self.columns.append(Hint(self,(x+1,0)))
        for y in range(size[1]):
            row=Hint(self,(0,y+1))
            self.rows.append(row)
            for x in range(size[0]):
                Cell(self,(self.columns[x],row))

class App(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.geometry('500x350')
        self.master.title('Griddler')
        tk.Label(self,text='Griddler',font='Mono 15 bold').grid(pady=20,row=1,column=1,columnspan=2)
        buttons=tk.Frame(self)
        buttons.grid(column=2,row=2,rowspan=2,padx=10)
        tk.Button(buttons,width=12,text='Blank',command=lambda:self.blank((10,10))).grid()
        tk.Button(buttons,width=12,text='Export hints',command=self.exportHints).grid()
        tk.Button(buttons,width=12,text='Import hints',command=self.importHints).grid()
        self.grid=None

    def blank(self,size):
        if self.grid:
            self.grid.destroy()
        self.grid=GameGrid(self,size)
        self.grid.grid(row=2,column=1,padx=20)

    def exportHints(self):
        out=str(len(self.grid.columns))+'x'+str(len(self.grid.rows))+'\n'
        for hint in self.grid.columns+self.grid.rows:
            out+=','.join(str(value) for value in hint.count())+'\n'
        with open(dirname(__file__)+'/hints.txt','w') as file:
            file.write(out)
            return True
        return False

    def importHints(self):
        with open(PATH+'/hints.txt','r') as file:
            size=file.readline()[:-1].split('x')
            size[0]=int(size[0])
            size[1]=int(size[1])
            data=file.readlines()
            if not self.grid:
                self.blank((size[0],size[1]))
            else:
                if size[0]!=len(self.grid.columns) or size[1]!=len(self.grid.rows):
                    self.blank((size[0],size[1]))
            i=0
            for values in data[:size[0]]:
                self.grid.columns[i].update(values[:-1].split(','))
                i+=1
            i=0
            for values in data[size[0]:]:
                self.grid.rows[i].update(values[:-1].split(','))
                i+=1



App().mainloop()
