from constants import Constants
from tkinter import *
from tkinter import ttk
import dateparser
from utils import FileUtils

import numpy as np

class Body(Frame):

    TOPSIZE = 40

    def __init__(self, master):
        self.master = master
        self.active_frame = 'table'

        super().__init__(master=self.master)
        self.pack_propagate(False)
        self.pack(fill=X)

        self.frames = {
            'table': Table(master=self, topsize=self.TOPSIZE),
            'graph': Graph(master=self, topsize=self.TOPSIZE)
        }

        self.frames[self.active_frame].pack_r()

    def resize(self, **kwargs): 
        self.config(height=kwargs['height'])
        self.frames[self.active_frame].resize(height=kwargs['height'])

    def swap(self, mode):
        self.inactive_frame = self.active_frame
        self.active_frame = mode
        self.change_pack()

    def change_room(self, room:str):
        self.frames[self.active_frame].set_room(room.replace('Salle ', ''))

    def change_pack(self):
        self.frames[self.inactive_frame].pack_f()
        self.frames[self.active_frame].pack_r()

class Table(Frame):

    def __init__(self, **kwargs):
        self.master = kwargs['master']
        self.topsize = kwargs['topsize']

        self.init_ui()

    def init_ui(self):
        super().__init__(master=self.master)
        self.pack_propagate(False)

        # Top frame
        self.top_frame = Frame(self, height=self.topsize)
        self.top_frame.pack(side=TOP, fill=X)

        self.select_date = ttk.Combobox(self.top_frame)
        self.select_date.place(relx=.5, rely=.5, anchor=CENTER)
        dates = []
        [dates.append(dateparser.parse(f'il y a {k} jours').date()) for k in range(30)]
        self.select_date['value'] = dates
        self.select_date.current(0)
        self.date = dates[0]
        self.select_date.bind("<<ComboboxSelected>>", self.__set_date)

        # Table frame
        self.table_frame = Frame(self)
        self.table_frame.pack(side=TOP, fill=BOTH)

        self.table = ttk.Treeview(self.table_frame)
        self.table['columns'] = ('date', 'heure', 'salle', 'température')

        self.table.column("#0", width=0,  stretch=NO) 
        self.table.heading("#0",text="",anchor=CENTER)
        for k in self.table['columns']:
            self.table.column(k, anchor=CENTER)
            self.table.heading(k, text=f"{k[0:1].upper()}{k[1:]}", anchor=CENTER)
        self.scroolbarvert = ttk.Scrollbar(self.table_frame, orient=VERTICAL, command=self.table.yview)
        self.scroolbarvert.pack(side=RIGHT, fill=Y)
        self.table.config(yscrollcommand=self.scroolbarvert.set)

        self.table.pack(fill=BOTH)

    def set_room(self, room):
        self.room = room
        self.__afficher_table()

    def __set_date(self, event):
        self.date = self.select_date.get()
        self.__afficher_table()

    def __afficher_table(self):
        try:
            lst = FileUtils.get_csv_list(f'../../data/{self.room}.csv', str(self.date))
        except: pass
        for i in self.table.get_children():
            self.table.delete(i)
        for k in lst:
            self.table.insert(parent='', index=END ,values=k)

    def pack_r(self): self.pack(side=TOP, padx=2, pady=2, fill=X)

    def pack_f(self): self.pack_forget()

    def resize(self, **kwargs): 
        self.config(height=kwargs['height'])
        self.table.config(height=kwargs['height'])

class Graph(Frame):

    def __init__(self, **kwargs):
        self.master = kwargs['master']
        self.topsize = kwargs['topsize']

        self.init_ui()

    def init_ui(self):

        super().__init__(self.master)
        self.pack_propagate(False)

        # Top frame
        self.top_frame = Frame(self, height=self.topsize)
        self.top_frame.pack(side=TOP, fill=X)

        # Graph frame
        self.graph_frame = Frame(self, highlightbackground=Constants.BLACK, highlightthickness=2)
        self.graph_frame.pack(side=TOP, fill=BOTH)


    def pack_r(self): self.pack(side=TOP, padx=2, pady=2, fill=X)

    def pack_f(self): self.pack_forget()

    def set_room(self, room):
        self.room = room
        self.__afficher_graph()
        
    def __afficher_graph(self): 
        pass

    def resize(self, **kwargs): 
        self.config(height=kwargs['height'])
        self.frame.config(height=kwargs['height'])