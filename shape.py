import tkinter as tk
from shape_type import ShapeType


class Shape(tk.Canvas):
    type = ShapeType.EMPTY

    def __init__(self, frame, **kw):
        super().__init__(frame, width=100, height=100, bg='white', **kw)
        self.create_rectangle(0, 0, 100, 100, fill='#0052cc')
        self.create_oval(5, 5, 95, 95, fill='white')

    def set_type(self, type):
        self.type = type
        if type == ShapeType.EMPTY:
            self.create_oval(5, 5, 95, 95, fill='white')
        elif type == ShapeType.RED:
            self.create_oval(5, 5, 95, 95, fill='red')
        elif type == ShapeType.YELLOW:
            self.create_oval(5, 5, 95, 95, fill='yellow')

    def get_type(self):
        return self.type
