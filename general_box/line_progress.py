import re
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from utils.dispatcher import GeneralColor
from kivymd.color_definitions import colors


class LineProgressBar(MDBoxLayout):
    """class for rendering the percentage"""
    def __init__(self, **kwargs):
        super(LineProgressBar, self).__init__(**kwargs)
        self.thickness = 25
        self.start = 0
        self.list_rect = []
        self.label = MDLabel(
            text="",
            font_size=18,
            line_height=1.0,
            halign='center',
            pos_hint={'center_y': -.1},
        )
        self.add_widget(self.label)

    def draw_init(self, list_article, summa):
        self.remove()
        self.label.text = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1 ", "%d" % summa) + ' ₽'
        if len(list_article) > 0:
            for item in list_article:
                self.draw(item[0], item[1])
        else:
            self.draw(GeneralColor.grey, 100)

    def draw_begining(self, color=GeneralColor.grey):
        """initial drawing of the sector"""
        self.begin_pos = (self.pos[0] + 10, self.pos[1] + 20)
        self.begin_size = (self.size[0] - 20, 15)
        self.rect_width = self.begin_size[0]

        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle()
            self.rect.pos = self.begin_pos
            self.rect.size = self.begin_size

    def draw(self, color, size_line):
        size_line = self.rect_width / 100 * size_line - 1
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle()
            self.rect.pos = (self.begin_pos[0] + self.start, self.begin_pos[1])
            self.rect.size = (size_line, self.begin_size[1])
            self.list_rect.append(self.rect)
        self.start += size_line + 2

    def on_touch_down(self, touch):
        for item in self.list_rect:
            pass

    def remove(self):
        with self.canvas.before:
            self.canvas.before.clear()
        self.start = 0
        self.label.text = ''
