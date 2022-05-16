from tkinter import Tk
from header import Header
from body import Body
from footer import Footer

class MainWindow(Tk):

    default_height = 540
    default_width = 960

    def __init__(self):

        self.init_ui()

    def init_ui(self):
        super().__init__()
        self.title('Température de l\'iut')
        self.geometry(f'{self.default_width}x{self.default_height}')
        self.minsize(750, 540)

        self.header_height, self.footer_height = 40, 50
        self.frames = {
            'header': Header(self, height=self.header_height),
            'body': Body(self),
            'footer': Footer(self, height=self.footer_height)
        }

        # self.frames['header'].signals['mode'].connect(self.frames['body'].swap)
        self.frames['header'].signals['mode'].connect(self.__resize_)
        self.frames['header'].signals['room'].connect(self.frames['body'].change_room)

        self.bind("<Configure>", self.__resize)
        self.update()

    def __resize_(self, str):
        self.__resize()

    def __resize(self, event=None):
        if event != None:
            if event.widget == self:
                body_height = self.winfo_height() - (self.header_height + self.footer_height)
                self.frames['body'].resize(height=body_height)
        else:
            body_height = self.winfo_height() - (self.header_height + self.footer_height)
            self.frames['body'].resize(height=body_height)

    def run(self):
        self.mainloop()
