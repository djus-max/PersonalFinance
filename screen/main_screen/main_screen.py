from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton

# my modules
from utils.dispatcher import EventControl
from general_box.date_choice import BoxDateDetail, BoxDate

from datetime import date


class DownBox(MDBoxLayout):
    root = ObjectProperty()

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if (self.root.flag_position_box == 'DOWN') and (touch.osy < 0.09) and \
                    ((touch.psy - touch.osy) > 0.1):
                self.root.moving_widget_up()

            if (self.root.flag_position_box == 'UP') and \
                    (0.65 > touch.osy > 0.55) and ((touch.osy - touch.psy) > 0.2):
                self.root.moving_widget_down()


class ButtonPlus(MDIconButton):
    pass


class ButtonPlusHight(ButtonPlus):
    pass


class ButtonPlusLite(ButtonPlus):
    pass


class MainScreen(Screen):
    """ Главный экран"""
    flag_position_box = 'DOWN'  # флаг позиции бокса с подробностями выписки по счету
    circle_progress_bar = ObjectProperty(None)
    up_widget = ObjectProperty(None)
    centr_widget = ObjectProperty(None)
    down_widget = ObjectProperty(None)
    choice_account = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        EventControl.main_screen = self
        self.__list_article = []
        self.__summa = 0
        self.begin_settings()

    def begin_settings(self):
        week_day = date.today()
        label_text = f"{week_day.strftime('%d')} {week_day.strftime('%B')}"
        BoxDate.main.change_label_text_date(label_text)
        self.data_for_query = {
            'id_account': 0,
            'date': week_day,
            'category': EventControl.categories,
        }

    def default_settings(self):
        self.data_for_query.update({'category': EventControl.categories})
        EventControl.choice_account_main.query_info_account()
        self.query_data()

    def default_settings_back(self):
        pass

    def set_data_for_query(self, **kwargs):
        for key, value in kwargs.items():
            self.data_for_query[key] = value
        self.query_data()

    def query_data(self):
        try:
            if len(self.data_for_query['date']):
                result, self.__summa = EventControl.database_outer.select_all_article_range(self.data_for_query)
        except TypeError:
            result, self.__summa = EventControl.database_outer.select_all_article(self.data_for_query)
        fun = self.query_data_group
        EventControl.thread_popup().new_popup(fun, result=result, summa=self.__summa)

    def query_data_group(self, result, summa):
        self.__list_article = self.ids.article_box.set_article(result, summa)
        self.circle_progress_bar.draw_init(self.__list_article, self.__summa)
        if self.flag_position_box == 'UP':
            self.ids.line_progress.draw_init(self.__list_article, self.__summa)

    def query_detail_data(self, instance, icon_group_id):
        data_for_query = {
            'id_account': self.data_for_query['id_account'],
            'date': self.data_for_query['date'],
            'category': self.data_for_query['category'],
            'icon_group_id': icon_group_id,
        }
        try:
            if len(data_for_query['date']):
                result, self.__summa_detail = EventControl.database_outer.select_detail_article_range(data_for_query)
        except TypeError:
            result, self.__summa_detail = EventControl.database_outer.select_detail_article(data_for_query)

        fun = instance.set_article_detail_group
        EventControl.thread_popup().new_popup(fun, result=result, summa=self.__summa_detail)

    def moving_widget_up(self):
        """ increasing the height of the widget and removing the button itself """
        self.centr_widget.size_hint_y = 0.2
        self.down_widget.size_hint_y = 0.65
        self.flag_position_box = 'UP'
        self.ids.scroll_box.scroll_y = 1
        BoxDateDetail.line_color_init()
        self.ids.box_for_button.clear_widgets()
        self.ids.box_for_button.add_widget(ButtonPlusLite())
        self.ids.line_progress.draw_begining()
        self.ids.line_progress.draw_init(self.__list_article, self.__summa)
        self.circle_progress_bar.canvas.opacity = 0
        self.ids.scroll_box.scroll_y = 1

    def moving_widget_down(self, ):
        self.ids.centr_widget.size_hint_y = 0.5
        self.ids.down_widget.size_hint_y = 0.3
        self.flag_position_box = 'DOWN'
        BoxDateDetail.line_color_init()
        self.ids.box_for_button.clear_widgets()
        self.ids.box_for_button.add_widget(ButtonPlusHight())
        self.ids.line_progress.remove()
        self.circle_progress_bar.canvas.opacity = 1
        self.ids.scroll_box.scroll_y = 1
