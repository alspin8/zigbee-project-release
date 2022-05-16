from tkinter.ttk import Combobox
from constants import Constants
from tkinter import *
import PySignal

class Header(Frame):

    buttonsleft_text = ["1h", "3h", "6h", "12h", "24h", "7d", "15d", "All"]

    def __init__(self, master, **kwargs):
        self.master = master
        self.height = kwargs['height']

        self.rooms = [
            'Salle D098',
            'Salle D092',
            'Salle D068'
        ]

        self.signals = PySignal.SignalFactory()
        self.signals.register('mode')
        self.signals.register('room')
        
        self.display_mode_text = StringVar()

        self.init_ui()

    def init_ui(self):
        super().__init__(master=self.master, height=self.height)
        self.pack_propagate(False)
        self.pack(side=TOP, padx=2, pady=2, fill=X)

        self.room = Label(self, text='Choisissé une salle')
        self.room.place(relx=.5, rely=.5, anchor=CENTER)

        self.combo_room = Combobox(self, values=self.rooms, state='readonly')
        self.combo_room.bind("<<ComboboxSelected>>", self.__selected_room)
        self.combo_room.pack(side=LEFT, padx=2)

        self.display_mode = Button(self, textvariable=self.display_mode_text, command=self.__change_mode, width=2)
        self.display_mode_text.set('Graph')
        self.display_mode.pack(side=LEFT)

    def __selected_room(self, event):
        self.room['text'] = self.combo_room.get()
        self.signals['room'].emit(self.room['text'])
    
    def get_room(self): return self.combo_room.get()

    def __change_mode(self):
        if self.display_mode_text.get() == 'Graph':
            self.signals['mode'].emit('graph')
            self.display_mode_text.set('List')
        elif self.display_mode_text.get() == 'List':
            self.signals['mode'].emit('table')
            self.display_mode_text.set('Graph')