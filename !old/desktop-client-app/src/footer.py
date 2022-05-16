from asyncio import constants


from constants import Constants
from tkinter import *

class Footer(Frame):

    def __init__(self, master, **kwargs):
        self.master = master
        self.height = kwargs['height']

        self.init_ui()

    def init_ui(self):
        super().__init__(master=self.master, height=self.height, highlightthickness=2, highlightbackground=Constants.BLACK)
        self.pack_propagate(False)
        self.pack(side=TOP, padx=2, pady=2, fill=X)