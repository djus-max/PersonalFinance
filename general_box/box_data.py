from ast import Pass
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior
from kivy.uix.behaviors.button import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker
from kivy.properties import ObjectProperty, ColorProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle

from utils.dispatcher import GeneralColor
from datetime import datetime, date, timedelta

import locale
locale.setlocale(locale.LC_ALL, '')


class BoxForData(MDBoxLayout):
    root_screen = ObjectProperty()

    def build_box(self, box_detail):
        list_data = BoxForData.check_current_data()
        for item in list_data:
            box = box_detail(
                self.root_screen,
                text_date=item['date'],
                text_name=item['name'],
                root_box=self,
            )
            self.add_widget(box)
        box = BoxPicker(box_detail)
        self.add_widget(box)

    @classmethod
    def check_current_data(cls):
        today = date.today()
        yesterday = today - timedelta(days=1)
        day_before_yesterday = today - timedelta(days=2)
        list_data = [
            {
                'name': 'Сегодня',
                'date': today,
            },
            {
                'name': 'Вчера',
                'date': yesterday,
            },
            {
                'name': 'Позавчера',
                'date': day_before_yesterday,
            },
        ]
        return list_data


class BoxForDataArticle(BoxForData):
    label_text_data: ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_box(self):
        box_detail = BoxForDataDetailArticle
        super().build_box(box_detail)
        BoxForDataDetailArticle.change_color()


class BoxForDataTransfer(BoxForData):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_box(self):
        box_detail = BoxForDataDetailTransfer
        super().build_box(box_detail)


class BoxForDataDetail(MDGridLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    active_color_box = GeneralColor.dark_grey
    inactive_color_box = GeneralColor.grey
    canvas_color = ListProperty()

    def __init__(self, root_screen, text_date, text_name, **kwargs):
        super().__init__()
        self.__class__.root_box = kwargs['root_box']
        self.root_screen = root_screen
        self.date = text_date
        self.ids.text_date.text = f"{text_date.strftime('%-d.%m')}\n{text_date.strftime('%a')}"
        self.ids.text_date_name.text = text_name
        if text_name == 'Позавчера':
            self.__class__.work_inctance = self

    @classmethod
    def default_settings(cls):
        cls.choice_instance = ObjectProperty(None)
        cls.default_text_for_data()
        cls.change_color()
        cls.flag_date_picker = False

    @classmethod
    def default_text_for_data(cls):
        list_data = BoxForData.check_current_data()
        for number, instance in enumerate(cls.list_data):
            instance.ids.text_date.text = f"{list_data[number]['date'].strftime('%-d.%m')}\n{list_data[number]['date'].strftime('%a')}"
            instance.ids.text_date_name.text = list_data[number]['name']
            instance.date = list_data[number]['date']

    @classmethod
    def transition_settings(cls, date):
        cls.default_text_for_data()
        # FIXME
        # list_data = BoxForData.check_current_data()
        for number, instance in enumerate(cls.list_data):
            # instance.ids.text_date.text = f"{list_data[number]['date'].strftime('%-d.%m')}\n{list_data[number]['date'].strftime('%a')}"
            # instance.ids.text_date_name.text = list_data[number]['name']
            # instance.date = list_data[number]['date']
            if date == instance.date:
                cls.choice_instance = instance
                cls.change_color()
                return

        instance.ids.text_date.text = f"{date.strftime('%-d.%m')}\n{date.strftime('%a')}"
        instance.ids.text_date_name.text = 'Выбранная'
        instance.date = date
        cls.choice_instance = cls.work_inctance
        cls.flag_date_picker = True
        cls.change_color()

    def choice_data(self, value: str):
        self.ids.text_date.text = f"{value.strftime('%-d.%m')}\n{value.strftime('%a')}"
        self.ids.text_date_name.text = 'Выбранная'
        self.date = value
        self.__class__.choice_instance = self
        self.__class__.change_color()
        self.__class__.flag_date_picker = True
        self.root_screen.data_for_query.update({'date': self.date})

    def pick_data(self):
        self.__class__.choice_instance = self
        self.__class__.change_color()
        self.root_screen.data_for_query.update({'date': self.date})
        if self.__class__.flag_date_picker:
            self.__class__.default_text_for_data()
            self.__class__.flag_date_picker = False

    def color_box_date(self, color):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            RoundedRectangle(
                pos=self.pos, size=self.size,
                radius=[(10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0)]
            )

    @classmethod
    def change_color(cls):
        for item in cls.list_data:
            if item != cls.choice_instance:
                item.canvas_color = cls.inactive_color_box
            else:
                item.canvas_color = cls.active_color_box


class BoxForDataDetailArticle(BoxForDataDetail):
    choice_instance = ObjectProperty()
    flag_date_picker = False
    root_screen = ObjectProperty()
    list_data = []

    def __init__(self, root_screen, text_date, text_name, **kwargs):
        self.__class__.list_data.append(self)
        super().__init__(root_screen, text_date, text_name, **kwargs)

    @classmethod
    def change_color(cls):
        for item in cls.list_data:
            if item != cls.choice_instance:
                item.canvas_color = cls.inactive_color_box
            else:
                item.canvas_color = cls.active_color_box
        cls.root_box.label_text_data.text_color = GeneralColor.text_color_global


class BoxForDataDetailTransfer(BoxForDataDetail):
    choice_instance = ObjectProperty()
    flag_date_picker = False
    root_screen = ObjectProperty()
    list_data = []

    def __init__(self, root_screen, text_date, text_name, **kwargs):
        self.__class__.list_data.append(self)
        super().__init__(root_screen, text_date, text_name, **kwargs)


class BoxPicker(MDGridLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):

    def __init__(self, box_detail, **kwargs):
        super().__init__(**kwargs)
        self.box_detail = box_detail

    def show_date_picker(self):
        date_dialog = MDDatePicker(title='Выберите дату')
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        # FIXME
        self.box_detail.work_inctance.choice_data(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show(self, value):
        pass
