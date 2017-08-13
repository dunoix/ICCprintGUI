import tkinter as tk
from tkinter import ttk
from dbInteraction import sqlDB


import os, time, re, pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import CP, Compnd, Block

class Main(tk.Frame):
    def __init__(self):
        self.win = tk.Tk()
        self.createWidgets()
        self.db = sqlDB()
        
    def dbSearch(self):
        x = self.treeview.get_children()
        for item in x:
            self.treeview.delete(item)
            
        bname = self.BlockName.get()
        datalist = self.db.searchByBlock(bname)
        if len(datalist) > 0:
            print (datalist)
            for i in range(len(datalist)):
                print (i)
                self.treeview.insert('', 'end', text = i+1, values = (datalist[i][0], datalist[i][1],datalist[i][2], datalist[i][3]))
    	


    def createWidgets(self):

        # ---------TOP FRAME "Search"-----------------------
        self.search = ttk.LabelFrame(self.win, text="Search")
        self.search.grid(column=0, row=0, padx=8, pady=4)


        self.aLabel = ttk.Label(self.search, text="Compound:")
        self.aLabel.grid(column=0, row=0, sticky = tk.W)
        
        self.aLabel = ttk.Label(self.search, text="Block:")
        self.aLabel.grid(column=1, row=0, sticky = tk.W)

        # Adding a Textbox Entry widget for Compound name
        self.CompName = tk.StringVar()
        self.nameEntered = ttk.Entry(self.search, width=20, textvariable=self.CompName)
        self.nameEntered.grid(column=0, row=1, sticky = tk.W)
        
        # Adding a Textbox Entry widget for Block name
        self.BlockName = tk.StringVar()
        self.nameEntered = ttk.Entry(self.search, width=20, textvariable=self.BlockName)
        self.nameEntered.grid(column=1, row=1, sticky = tk.W)
        

        # Adding a Button
        self.action = ttk.Button(self.search, text="Search", command=self.dbSearch)
        self.action.grid(column=2, row=1, sticky = tk.W)
        #action.configure(state='disabled')    # Disable the Button Widget

        # Place cursor into name Entry
        self.nameEntered.focus()


        
        # ---------TOP FRAME "Results"-----------------------
        self.results = ttk.LabelFrame(self.win, text="Results")
        self.results.grid(column=0, row=1, padx=8, pady=4)


        self.tree = ttk.Treeview(self.results, columns = ('CP', 'Compound', 'Block', 'Type'))
        self.tree.heading('#0', text = '#')
        self.tree.heading('#1', text = 'CP')
        self.tree.heading('#2', text = 'Compound')
        self.tree.heading('#3', text = 'Block')
        self.tree.heading('#4', text = 'Type')
        self.tree.column('#0', stretch = tk.YES)
        self.tree.column('#1', stretch = tk.YES)
        self.tree.column('#2', stretch = tk.YES)
        self.tree.column('#3', stretch = tk.YES)
        self.tree.column('#4', stretch = tk.YES)
        self.tree.grid(row=0, columnspan=4, sticky = 'nsew')
        self.treeview = self.tree



        # ---------TOP FRAME "Parameters"-----------------------
        self.parameters = ttk.LabelFrame(self.win, text="Parameters")
        self.parameters.grid(column=0, row=2, padx=8, pady=4)


        # Config Canvas
        self.canvas = tk.Canvas(self.parameters, borderwidth = 0)
        self.canvas.grid(column=0, row=0, sticky = tk.W)
        self.frame = tk.Frame(self.canvas, background = "#ffffff")
        self.vsb = tk.Scrollbar(self.parameters, orient = "vertical", command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.vsb.set)

        self.vsb.grid(column=1, row=0, sticky = "ns")
        self.canvas.create_window((4,4), window=self.frame, anchor = "nw", tags = "self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def populate(self):
        res = self.session.query(Block).filter(Block.bname == self.BlockName.get()).first()
        data = json.loads(res.bdata)
        for lineNo in range(len(data)):
            line = data[lineNo]
            parameter_label = tk.Label(self.frame, text = line[0], anchor = "e", width = 7)
            parameter_entry = tk.Entry(self.frame, width = 50)
            parameter_entry.insert(tk.END, line[1])

            parameter_label.grid(row=lineNo+2, column=0, sticky=tk.W)
            parameter_entry.grid(row=lineNo+2, column=1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def Search(BlockName):
        res = session.query(Block).filter(Block.bname == BlockName).first()
        return (json.loads(res.bdata))

# E100U_A13600:ESV212

#======================
# Start GUI
#======================
oop = Main()
oop.win.mainloop()
