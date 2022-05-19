from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from functools import partial

# my module import
from utils.dispatcher import EventControl, GeneralColor
from general_box.header import Header
from general_box.сhoice_сategory import BoxForCheck
from general_box.box_data import BoxForDataDetailArticle


class HeaderAddArticle(Header):
    """ Шапка экрана"""
    header_label = StringProperty('Создайте категорию')
    old_screen = ObjectProperty(None)
    old_screen_str = StringProperty('MainScreen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_screen = EventControl.main_screen


class AddArticleScreen(Screen):
    """ Экран добавления статей"""
    main_self = ObjectProperty()
    choice_account = {}
    data_for_query = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__class__.main_self = self
        self.ids.check_costs.ids.label.text = 'расходы'
        self.ids.check_income.ids.label.text = 'доходы'
        self.flag = False
        # построение дат
        self.ids.box_for_data.build_box()
        self.default_settings_data()

    def overload_icons(self):
        self.data_for_query.update({
            'icon_category_id': None,
            'icon_group_id': None,
        })
        self.flag = False
        if self.ids.box_group.ids.check_group.active:
            self.ids.box_category.default_settings()
            self.ids.box_group.build_icon(flag=self.flag)
        else:
            self.ids.box_category.build_icon(flag=self.flag)

    def default_settings_back(self):
        pass
        # FIXME пересмотреть код
        # в любом случае
        # self.flag = False
        # self.ids.box_article.ids.box_for_icon_article.clear_widgets()
        # self.ids.scroll_box.scroll_y = 1
        # self.default_settings_data()
        # self.ids.box_choice_for_account.label_default()
        # self.clear_text_label()
        # self.ids.label_text_data.text_color = GeneralColor.text_color_global
        # BoxForDataDetailArticle.default_settings()'''

    def default_settings_data(self):
        self.data_for_query = {
            'id_account': '',
            'date': '',
            'icon_category_id': None,
            'summa': '',
            'comment': '',
            'category': EventControl.categories,
            'icon_group_id': None,
        }

    def default_settings(self, **kwargs):
        self.flag = False
        self.default_settings_data()
        self.ids.box_category.build_icon()
        self.ids.box_group.default_settings_box()
        self.ids.scroll_box.scroll_y = 1
        self.ids.box_choice_for_account.label_default()
        self.clear_text_label()
        self.ids.label_text_data.text_color = GeneralColor.text_color_global
        BoxForDataDetailArticle.default_settings()
        if EventControl.categories == 'costs':
            self.ids.check_costs.ids.check.active = True
            BoxForCheck._active_check_box = self.ids.check_costs.ids.check
        elif EventControl.categories == 'income':
            self.ids.check_income.ids.check.active = True
            BoxForCheck._active_check_box = self.ids.check_income.ids.check

    def clear_text_label(self):
        self.ids.text_field_summa.text = ''
        self.ids.text_field_comment.text = ''

    @classmethod
    def set_info(cls, **kwargs):
        for key, value in kwargs.items():
            cls.data_for_query[key] = value

    def query_insert_article(self):
        """Validating all required fields and submitting data to the database"""
        if self.data_for_query['summa'] == '':
            self.ids.scroll_box.scroll_to(self.ids.text_field_summa, padding=20, animate={'d': .2, 't': 'in_quad'})
            self.ids.text_field_summa.error = True
            self.ids.text_field_summa.focus = True
            return
        elif self.data_for_query['id_account'] == '':
            self.ids.scroll_box.scroll_to(self.ids.box_choice_for_account, padding=20, animate={'d': .15, 't': 'in_circ'})
            Clock.schedule_once(partial(self.ids.box_choice_for_account.change_label_error), .3)    # self.ids.box_choice_for_account.change_label_error()
            return
        elif self.ids.box_group.ids.check_group.active and self.data_for_query['icon_group_id'] is None:
            self.ids.scroll_box.scroll_to(self.ids.box_group, padding=20, animate={'d': .15, 't': 'in_circ'})
            self.ids.box_group.ids.label_text_icon.text_color = GeneralColor.bright_red
            self.ids.box_group.ids.label_text_icon.wobble()
            return
        elif self.data_for_query['icon_category_id'] is None:
            self.ids.scroll_box.scroll_to(self.ids.box_category, padding=20, animate={'d': .15, 't': 'in_circ'})
            self.ids.box_category.ids.label_text_icon.text_color = GeneralColor.bright_red
            self.ids.box_category.ids.label_text_icon.wobble()
            return
        elif self.data_for_query['date'] == '':
            self.ids.label_text_data.text_color = GeneralColor.bright_red
            self.ids.label_text_data.wobble()
            return

        # Запись в БД статьи расхода или дохода
        EventControl.database_outer.query_insert_articlre(self.data_for_query)
        # EventControl().categories = self.data_for_query['category']
        # EventControl.manager_instance.transition_screen("MainScreen")
        EventControl.manager_instance.new_screen_transition(EventControl.main_screen, "MainScreen", 'default')

    def add_widget_icon_all(self, header_name):
        EventControl.manager_instance.icon_all_screen.default_settings(header_name=header_name, data_for_query=self.data_for_query)
        self.add_widget(EventControl.manager_instance.icon_all_screen, index=0)
        self.ids.widget_one.disabled = True

    def delete_widget_icon_category(self):
        self.remove_widget(EventControl.manager_instance.icon_all_screen)
        # TODO сделать таймер
        self.ids.widget_one.disabled = False
        self.ids.button_add_article.md_bg_color = GeneralColor.header_color

    def transition_back_after_save(self, data_for_query, icon_id_after_insert):
        if data_for_query['group']:
            self.ids.box_group.build_icon(flag=True)
            self.ids.box_category.build_icon(selection=icon_id_after_insert)
            self.data_for_query.update({
                'icon_category_id': None,
                'icon_group_id': icon_id_after_insert,
            })
        elif data_for_query['group'] is False:
            self.ids.box_category.build_icon(
                flag=True,
                selection=data_for_query['group_id']
            )
            self.data_for_query.update({
                'icon_category_id': icon_id_after_insert,
            })
        self.remove_widget(EventControl.manager_instance.icon_all_screen)
        EventControl.manager_instance.icon_all_screen.default_settings_back()
        # TODO сделать таймер
        self.ids.widget_one.disabled = False
        self.ids.button_add_article.md_bg_color = GeneralColor.header_color
