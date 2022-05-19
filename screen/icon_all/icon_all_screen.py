from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty

# my module import
from utils.dispatcher import EventControl, GeneralColor
from general_box.header import Header


class HeaderAllIcon(Header):
    """ Шапка скрина"""
    header_label = StringProperty('')
    old_screen = ObjectProperty(None)
    old_screen_str = StringProperty('AddArticleScreen')
    root_screem = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_screen = EventControl.add_article_screen


class IconAllScreen(Screen):
    """ Экран добавления статьи расхода или дохода"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.header.color_header_canvas = GeneralColor.colorless
        self.ids.centr_box.color_canvas = GeneralColor.colorless
        self.data_for_query = {
            'category': EventControl.categories,
            'title': '',
            'icon_name': '',
            'icon_color': '',
        }
        # Запрос к базе данных для выборки всех иконок (единожды)
        # result_query = EventControl.database_inner.select_icon_all('category')
        self.ids.box_category.build_icon()

    def default_settings_back(self):
        """default screen settings"""
        self.ids.text_category.error = False
        self.ids.text_category.text = ''
        self.ids.text_category.helper_text = ''
        # дефолтные настройки для цeлого бокса
        self.ids.box_category.default_settings_back()

    def default_settings(self, **kwargs):
        self.data_for_query = {
            'category': kwargs['data_for_query']['category'],
            'title': '',
            'icon_name': '',
            'icon_color': '',
            'group': False,
            'group_id': None,
        }
        if kwargs['header_name'] == 'category':
            header_label_name = 'Создание категории'
            self.data_for_query.update({'group_id': kwargs['data_for_query']['icon_group_id']})
        elif kwargs['header_name'] == 'group':
            header_label_name = 'Создание группы'
            self.data_for_query.update({'group': True})
        if kwargs['data_for_query']['category'] == 'costs':
            header_label_category = 'расходов'
        elif kwargs['data_for_query']['category'] == 'income':
            header_label_category = 'доходов'
        self.ids.header.header_label = f'{header_label_name} {header_label_category}'

    def query_insert_icon(self):
        """Validating all required fields and submitting data to the database"""
        if self.data_for_query['title'] == '':
            self.ids.text_category.error = True
            self.ids.text_category.focus = True
            self.ids.text_category.helper_text = 'Введите название'
            return
        elif self.data_for_query['icon_name'] == '':
            self.ids.box_category.ids.label_text_icon.text_color = GeneralColor.bright_red
            self.ids.box_category.ids.label_text_icon.wobble()
            return
        elif self.data_for_query['icon_color'] == '':
            self.ids.box_category.ids.label_text_color.text_color = GeneralColor.bright_red
            self.ids.box_category.ids.label_text_color.wobble()
            return
        icon_id_after_insert = EventControl.database_outer.query_insert_icon(self.data_for_query)
        fun = self.ids.header.old_screen.transition_back_after_save
        EventControl.thread_popup().new_popup(fun, data_for_query=self.data_for_query, icon_id_after_insert=icon_id_after_insert)

    def transition_back(self):
        # TODO придумать универсальный метод
        self.default_settings_back()
        self.ids.header.old_screen.delete_widget_icon_category()
