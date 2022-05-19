from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.core.text import Label as CoreLabel
from utils.dispatcher import GeneralColor
from utils.re_text import division_of_amount


class Progress(MDBoxLayout):
    pass


class CircularProgressBar(Progress):
    """class for rendering the percentage"""
    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        self.remove()
        self.thickness = 25
        self.label = CoreLabel(
            text="",
            font_size=18,
            shorten=True,
            shorten_from='center',
            text_size=(self.width + 10, None),
            line_height=1.0,
            halign='center'
        )

        # Initialise the texture_size variable
        self.texture_size = None
        self.refresh_text(summa=0)

    def draw_init(self, list_article, summa):
        self.refresh_text(summa)
        self.draw()
        start = 0
        for item in list_article:
            self.draw(item[0], start, item[1])
            start += item[1]
        self.draw_inner_color()

    def draw(self, color_bar=GeneralColor.grey, start=-1, finish=101):
        """ drawing part of sectors """
        start = 360 / 100 * start + 1
        finish = 360 / 100 * finish + start - 1
        self.size = '150sp', '150sp'
        self.pos = (Window.width / 2 - self.size[0] / 2, Window.height / 2 - self.size[1] / 2)

        with self.canvas:
            Color(*color_bar)
            Ellipse(pos=self.pos, size=self.size, angle_start=start, angle_end=finish)

    def draw_inner_color(self):
        """ filling the interior space with color """
        with self.canvas:
            Color(*(GeneralColor.white))
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),
                    size=(self.size[0] - self.thickness, self.size[1] - self.thickness))
            # Center and draw the progress text
            Color(*(GeneralColor.black))
            # added pos[0]and pos[1] for centralizing label text whenever pos_hint is set
            Rectangle(
                texture=self.label.texture, size=self.texture_size,
                pos=(self.size[0] / 2 - self.texture_size[0] / 2 + self.pos[0], self.size[1] / 2 - self.texture_size[1] / 2 + self.pos[1])
            )

    def refresh_text(self, summa):
        # Render the label
        summa = division_of_amount(summa)
        self.label.text = str(summa) + ' ₽ '
        self.label.refresh()
        # Set the texture size each refresh
        self.texture_size = list(self.label.texture.size)

    def remove(self):
        with self.canvas:
            self.canvas.clear()


class LineProgressBar(Progress):
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
        summa = division_of_amount(summa)
        self.label.text = str(summa) + ' ₽ '
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
