from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.carousel import MDCarousel
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.behaviors import CircularRippleBehavior, BackgroundColorBehavior
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.properties import ListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window

import math
from utils.dispatcher import GeneralColor

###########################################################
# ################# Общие классы ###########################


class BoxIconCarousel(MDCarousel):
    """ ids = box_icon_carousel"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_icon(self, result_query, info):
        # self.clear_widgets()  # FIXME
        self.list_index = {}    # Для постройки индекса
        _multi_size_hint_x, _sum_padding_left_right = self._general_sum_padding(info)
        number_of_icons, number = self._count_carousel(len(result_query), _multi_size_hint_x, _sum_padding_left_right)

        if len(result_query) <= 4:
            self.height = 85
        else:
            self.height = 160
        info['root_box'].ids.box_index.build_index(number)  # постройка индекса
        for index in range(number):
            # BoxForIcon
            box = info['box_for_icon'](result_query[(index * number_of_icons): ((index + 1) * (number_of_icons))], info, index=index)
            self.add_widget(box)

    def on_slide_complete(self, *args):
        """Switching a slide with icons and calling the drawing of the active slide"""
        for key, value in self.list_index.items():
            instance = value[0]
            if key != self.index:
                value[1] = 'inactive'
                instance.drow_canvas(instance.inactive_canvas)
            else:
                value[1] = 'active'
                instance.drow_canvas(instance.active_canvas)

    def _general_sum_padding(self, info):
        sum_padding = [0, 0, 0, 0]
        multi_size_hint_x = 1

        def count_pading(instance, sum_padding, multi_size_hint_x):
            while instance != info['root_box'].root_screen:
                try:
                    sum_padding = [a + b for a, b in zip(sum_padding, instance.padding)]
                    multi_size_hint_x = multi_size_hint_x * instance.size_hint[0]
                except Exception as ex:
                    pass
                finally:
                    instance = instance.parent
                    continue
            return sum_padding, multi_size_hint_x

        _instance = self
        _sum_padding, _multi_size_hint_x = count_pading(_instance, sum_padding, multi_size_hint_x)
        _sum_padding_left_right = _sum_padding[0] + _sum_padding[-1]
        return _multi_size_hint_x, _sum_padding_left_right

    def _count_carousel(self, length: int, multi_size_hint_x, sum_padding_left_right) -> int:
        """Counting the icons that fit in the window.
        Entering into the general variable the number of icons in two rows.
        """
        _width = Window.width * multi_size_hint_x
        number_of_icons = int((_width - sum_padding_left_right) / (50 + 15))
        number = math.ceil(length / (number_of_icons * 2))
        return number_of_icons * 2, number


class BoxForIcon(MDStackLayout):

    def __init__(self, result, info, *args, **kwargs):
        super().__init__()
        self.rows = 2
        self.spacing = 15
        self.begin_settings(result, info, *args, **kwargs)

    def begin_settings(self, result, info, *args, **kwargs):
        number_of_icons = self._calculations_maximum_of_icons()
        # добавление иконок для увеличения высоты бокса ,
        # что бы не перекрывали кнопку добавления категорий
        if kwargs['index'] == 0 and len(result) == number_of_icons:
            result.append([])
        if kwargs['index'] > 0 and len(result) <= number_of_icons:
            for i in range(number_of_icons - len(result) + 1):
                result.append([])

        for item in result:
            # BoxForIconDetail
            box = info['box_for_icon_detail'](item, info)
            self.add_widget(box)

    def _calculations_maximum_of_icons(self):
        number_of_icons = int((Window.width - 15) / (50 + 15))
        left_padding = ((Window.width - 15) - ((50 + 15) * number_of_icons)) / 2
        self.padding = (left_padding, 0, 0, 10)
        return number_of_icons


class BoxForIconDetail(MDGridLayout):
    color_canvas_after = ListProperty([1, 1, 1, 0])
    acive_icon = None

    def __init__(self, item, info, *args, **kwargs):
        super().__init__()
        self.begin_settings(item, info, *args, **kwargs)

    def begin_settings(self, item, info, *args, **kwargs):
        try:
            self.ids.icon_button.icon = item.icon_name
            self.ids.label.text = item.title
            self.data = item
        except Exception:
            self.disabled = True
            self.color_canvas_after = GeneralColor.white

    @classmethod
    def change_color_icon(cls, box_change, color=''):
        """Setting the icon color"""
        # box_change.change_label_error_color()
        try:
            # box_change.ids.box_icon_carousel.current_icon.icon_outer_color = color
            cls.acive_icon.ids.icon_button.md_bg_color = color
        except AttributeError:
            pass
        except ValueError:
            cls.acive_icon.ids.icon_button.md_bg_color = GeneralColor.grey
            return
        finally:
            box_change.main_screen.data_for_query.update({'icon_color': color})
            box_change.ids.label_text_color.text_color = GeneralColor.text_color_global


##########################################################
# ############## Классы индекса ###########################


class BoxForCanvas(FloatLayout, CircularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    """General class for drawing circles """

    def drow_canvas(self, color='', size_canvas=(8, 8)):
        self.canvas.clear()
        with self.canvas:
            Color(*color)
            self.rect = Ellipse(pos=self.pos, size=size_canvas)
        self.bind(pos=self.update_ellipse)

    def update_ellipse(self, *args):
        self.rect.pos = self.pos


class BoxIndex(MDBoxLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box_icon_carousel = ObjectProperty(None)

    def build_index(self, number):
        if number <= 1:
            return
        for index in range(number):
            box = BoxForCurrentIndex(self.box_icon_carousel, index)
            self.add_widget(box)


class BoxForCurrentIndex(BoxForCanvas):
    """class for rendering all indices under the carousel"""
    # pos_hint = {"center_x": 0.5,"center_y": 0.1}
    size_hint = (0.2, 0.2)
    active_canvas = GeneralColor.black                # TODO
    inactive_canvas = GeneralColor.grey

    def __init__(self, box_icon_carousel, index=0, **kwargs):
        super(BoxForCurrentIndex, self).__init__(**kwargs)
        if index == 0:
            active = 'active'
            self.drow_canvas(self.active_canvas)
        elif index > 0:
            active = 'inactive'
            self.drow_canvas(self.inactive_canvas)
        box_icon_carousel.list_index.update({index: [self, active]})

    def on_press(self):
        """обратная взаимосвязь с каруселью"""
        pass

    @classmethod
    def update_canvas(cls, index):
        for key, value in cls.list_index.items():
            self = value[0]
            if key != index:
                value[1] = 'inactive'
                self.drow_canvas(self.inactive_canvas)
            else:
                value[1] = 'active'
                self.drow_canvas(self.active_canvas)


############################################################
# ######################## Конец общих классов #############


############################################################
# #################### Класс выбора цыета ###################


class BoxForColor(MDGridLayout):
    """Class for rendering color selection"""
    list_color = [
        GeneralColor.bright_red,
        GeneralColor.bright_blue,
        GeneralColor.bright_green,
        GeneralColor.bright_yellow,
        GeneralColor.ligtly_blue,
        GeneralColor.violet,
        GeneralColor.ligtly_green,
    ]

    def __init__(self, *args, **kwargs):
        super(BoxForColor, self).__init__(*args, **kwargs)
        self.box_change = ObjectProperty()

    def build_canvas(self):
        for color in self.list_color:
            box = BoxForColorCanvas(self.box_change, color=color)
            self.add_widget(box)


class BoxForColorCanvas(BoxForCanvas):
    pos_hint = {"center_x": 0.5, "center_y": 1}
    size_hint = (1, 1)
    ripple_alpha = 0
    padding = 30, 0
    canvas_color = ListProperty()

    def __init__(self, box_change, color, **kwargs):
        super(BoxForColorCanvas, self).__init__(**kwargs)
        self.box_change = box_change
        self.drow_canvas(color=color, size_canvas=(35, 35))
        self.canvas_color = color

    def on_touch_down(self, touch):
        """Setting the icon color"""
        if self.pos[0] < touch.pos[0] < (self.pos[0] + 40):
            self.box_change._info['box_for_icon_detail'].change_color_icon(
                self.box_change,
                color=self.canvas_color
            )

    def drow_canvas(self, color='', size_canvas=(8, 8)):
        self.canvas.clear()
        with self.canvas:
            Color(*color)
            self.rect = Ellipse(pos=self.pos, size=size_canvas)
        self.bind(pos=self.update_ellipse)

    def update_ellipse(self, *args):
        self.rect.pos = self.pos


# #############Конец классов для выбора цвета ########
############################################################
