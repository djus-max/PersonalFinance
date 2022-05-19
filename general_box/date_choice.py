from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivymd.uix.picker import MDDatePicker
from datetime import date, timedelta
import arrow

from utils.dispatcher import EventControl, GeneralColor
from kivy.properties import ObjectProperty


class BoxDate(MDBoxLayout):
    main = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        BoxDate.main = self

    def change_label_text_date(self, value):
        self.ids.label_text_date.text = str(value)

    def change_arrow(self, instance):
        pass


class BoxForDate(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        list_data = [
            {
                'name': 'cегодня',
                'id': 'today',
            },
            {
                'name': 'неделя',
                'id': 'week',
            },
            {
                'name': 'месяц',
                'id': 'month',
            },
            {
                'name': 'год',
                'id': 'year',
            },
        ]
        for item in list_data:
            box = BoxDateDetail(text_date=item['name'], id=item['id'])
            self.add_widget(box)

        box = BoxPickerDateMain(text_date='дата', id='picker')
        self.add_widget(box)


class BoxArrow(MDBoxLayout, ButtonBehavior, BackgroundColorBehavior, RectangularRippleBehavior):
    pass


class BoxDateDetail(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    active_date = ''
    root_screen = ObjectProperty()

    def __init__(self, text_date, id, **kwargs):
        super().__init__(**kwargs)
        self.ids.text_date.text = text_date
        self.id = id
        if id == 'today':
            BoxDateDetail.active_date = self
            self.line_color_init(self, GeneralColor.black)
            self.ids.text_date.text_color = GeneralColor.black
        else:
            self.line_color_init(self, GeneralColor.colorless)

    def choice_date(self, instance):
        if instance == BoxDateDetail.active_date:
            return
        week_day = date.today()
        arrow_week_day = arrow.Arrow.fromdate(week_day)

        if instance.id == 'today':
            EventControl.main_screen.set_data_for_query(date=(week_day))
            label_text = f"{arrow_week_day.strftime('%d %B')} "
        else:
            if instance.id == 'week':
                start_date = arrow_week_day.floor("week")
                label_text = f"{start_date.strftime('%d %B')} - {arrow_week_day.strftime('%d %B')}"
                start_date = start_date.date()
            elif instance.id == 'month':
                start_date = arrow_week_day.floor("month")
                label_text = BoxDateDetail.month_name(int(arrow_week_day.strftime('%m')), 'ru')
                start_date = start_date.date()

            elif instance.id == 'year':
                year = date.today().isocalendar()[0]
                start_date = date(year, 1, 1)
                label_text = year

            EventControl.main_screen.set_data_for_query(date=(week_day, start_date))
            EventControl.main_screen.ids.scroll_box.scroll_y = 1

        BoxDate.main.change_label_text_date(label_text)
        BoxDateDetail.update_line_color(instance)

    @classmethod
    def update_line_color(cls, instance):
        cls.line_color_delete(cls.active_date)
        cls.active_date.ids.text_date.text_color = GeneralColor.dark_grey
        cls.active_date = instance
        cls.active_date.ids.text_date.text_color = GeneralColor.black
        cls.line_color_update(instance, GeneralColor.black)

    @classmethod
    def time_interval(cls, number: int):
        week_day = date.today()
        number_of_days = date.today().isocalendar()[number]
        start_date = date.today() - timedelta(days=number_of_days)
        EventControl.main_screen.set_data_for_query(date=(week_day, start_date))

    @classmethod
    def line_color_update(cls, instance=False, color=GeneralColor.black):
        if instance is False:
            instance = cls.active_date
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*color)
            Rectangle(
                pos=(instance.pos[0] + 10, instance.pos[1]),
                size=(instance.size[0] - 20, 3)
            )

    @classmethod
    def line_color_delete(cls, instance):
        instance.canvas.before.clear()

    @classmethod
    def line_color_init(cls, instance=False, color=GeneralColor.black):
        if instance is False:
            instance = cls.active_date
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*color)
            instance.rect = Rectangle()
        instance.bind(pos=instance.update_rectangle, size=instance.update_rectangle)

    def update_rectangle(self, *args):
        self.rect.pos = (self.pos[0] + 10, self.pos[1])
        self.rect.size = (self.size[0] - 20, 3)

    @staticmethod
    def month_name(num, lang):
        # FIXME change to ENUM
        en = [
            'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
            'october', 'november', 'december'
        ]
        ru = [
            'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь',
            'октябрь', 'ноябрь', 'декабрь'
        ]
        if lang == 'en':
            return en[num - 1]
        else:
            return ru[num - 1]


class BoxPickerDateMain(BoxDateDetail):

    def __init__(self, text_date, id, **kwargs):
        super().__init__(text_date, id)

    def choice_date(self, instance):
        date_dialog = MDDatePicker(title='Выберите дату')
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
        if instance == self.active_date:
            return
        BoxDateDetail.update_line_color(instance)

    def on_save(self, instance, week_day, date_range):
        EventControl.main_screen.set_data_for_query(date=(week_day))
        label_text = f"{week_day.strftime('%d')} {week_day.strftime('%B')}"
        BoxDate.main.change_label_text_date(label_text)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show(self, value):
        pass
