# -*- coding: utf-8 -*-
import concurrent.futures
from functools import partial

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.clock import Clock, mainthread
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.utils import asynckivy


# my modules
from settings import BeginConfiguration
from utils.thread_popup import ContentPopup
from utils.dispatcher import EventControl
from screen.main_screen.main_screen import MainScreen
from screen.add_article.add_article_screen import AddArticleScreen
from screen.all_account.all_account_screen import AllAccountScreen
from screen.add_transfer.add_transfer_screen import AddTransferScreen
from screen.icon_all.icon_all_screen import IconAllScreen
# from screen.add_icon.add_icon_screen import AddIconScreen
from screen.add_account_credit.add_account_screen import AddAccountScreen
from screen.detail_article.detail_article_screen import DetailArticle
# from screen.navigation_bar.navigation_bar import *
from screen.navigation_bar.navigation_bar import NavigationBar
# Общие модули
from screen.main_screen.box_detail import ArticleBox
from screen.add_article.box_icon import BoxGroupArticle
from screen.icon_all.box_icon import BoxCategoryIconAll
from screen.add_account_credit.box_icon import BoxChoiceIconAccounnt
from general_box.box_detail import AccountBox
from general_box.account_window import BoxChoiceAccountMain
from general_box.line_progress import LineProgressBar
from general_box.progress_bar import CircularProgressBar
from general_box.text_input import TextInputSumma
# вспомогиательные инструменты


class ScreenManagement(ScreenManager):
    """ pass """
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        EventControl.manager_instance = self
        self.adding_screen()
        self.__dialog = Popup(
            title="",
            separator_height=0,
            size_hint=(0.7, 0.2),
            opacity=1,
            auto_dismiss=False,
            background='./data/img/f.png',
            # type="custom",
            content=ContentPopup(),
        )

        # Вывод скрина для заполнения счета если в базе еще не созданны
        result = EventControl.database_outer.account_count()
        if result == 0:
            self.current = 'AddAccountScreen'
        else:
            self.current = 'MainScreen'      # MainScreen
            self.current_screen.default_settings()

    def adding_screen(self):
        """Инициализаия и добавление скринов"""
        # Главный скрин
        EventControl.main_screen = self.main_screen = MainScreen(name='MainScreen')
        self.add_widget(self.main_screen)

        # Скрины добавления статей рахода и его вспомогательных
        EventControl.add_article_screen = self.add_article_screen = AddArticleScreen(
            name='AddArticleScreen')
        self.add_widget(self.add_article_screen)
        # EventControl.add_icon_screen = self.add_icon_screen = AddIconScreen(name='AddIconScreen')
        # self.add_widget(self.add_icon_screen)
        EventControl.icon_all_screen = self.icon_all_screen = IconAllScreen(name='IconAllScreen')
        self.add_widget(self.icon_all_screen)

        # Скрин аккаунта и его дочерних
        EventControl.add_account_screen = self.add_account_screen = AddAccountScreen(name='AddAccountScreen')
        self.add_widget(self.add_account_screen)
        EventControl.all_account_screen = self.all_account_screen = AllAccountScreen(name='AllAccountScreen')
        self.add_widget(self.all_account_screen)
        EventControl.add_transfer_screen = self.add_transfer_screen = AddTransferScreen(name='AddTransferScreen')
        self.add_widget(self.add_transfer_screen)

    def transition_all_account_screen(self, screen):
        """ Переход на скрин со всеми счетами и переводами с боковой панели"""
        # current_last = self.current_screen
        self.current = screen
        self.current_screen.default_settings()

        # self.__event = Clock.schedule_interval(partial(self.loading_content), 0.05)

    def loading_content(self, dt):
        """ pass """
        instance = self.current_screen

        async def notify():
            await asynckivy.sleep(0)
            if instance.transition_progress == 1:
                instance.default_settings()
                Clock.unschedule(self.__event)

        asynckivy.start(notify())

    def new_screen_transition(self, new_screen, new_screen_str, new_screen_flag, **kwargs):
        """ Переход на скрин добавления перевода со скрина всех счетов"""

        '''self.__new_screen = new_screen
        self.__new_screen_str = new_screen_str
        self.__new_screen_flag = new_screen_flag
        self.__new_screen_data = new_screen_data'''

        '''self.current = self.__new_screen_str
        if self.__new_screen_flag == 'default':

            self.__new_screen.default_settings()

        elif self.__new_screen_flag == 'back':
            self.__new_screen.default_settings_back()
        elif self.__new_screen_flag == 'old':
            self.__new_screen.old_settings(self.__new_screen_data)'''

        # Clock.schedule_once(partial(self.__progress_popup), 0)
        # Clock.schedule_once(partial(self.start_tread), 0.1)

        Clock.schedule_once(partial(self.start_tread), 0)
        Clock.schedule_once(partial(self.__setting_new_parameters, new_screen, new_screen_str, new_screen_flag, **kwargs), 0.2)

    def start_tread(self, dt, **kw):
        executor = concurrent.futures.ThreadPoolExecutor()
        # f1 = executor.submit(self.pop_up1)  # this must be done on the main thread
        f2 = executor.submit(self.__progress_popup)
        # threading.Thread(target=partial(self.__setting_new_parameters)).start()

    def __progress_popup(self):
        """ Добавление спинера загрузки в главный поток"""
        self.__dialog.open()

    def __setting_new_parameters(self, new_screen, new_screen_str, new_screen_flag, dt, **kwargs):
        """ настройка новых параметров нового окна"""

        # async def notify():
        # await asynckivy.sleep(0)
        if new_screen_flag == 'default':
            # Clock.schedule_once(self.__new_screen.default_settings)
            new_screen.default_settings(**kwargs)
        elif new_screen_flag == 'back':
            new_screen.default_settings_back()
        elif new_screen_flag == 'old':
            new_screen.old_settings(**kwargs)

        # asynckivy.start(notify())
        # self.current = new_screen_str
        # for number in range(50000):
            # print(number)
        # Clock.schedule_once( self.transition_screen)  # pop_up2() must be done on the main thread
        Clock.schedule_once(partial(self.transition_screen, new_screen_str), 0.1)
        # Clock.schedule_once(partial(self.dismiss), 0.2)

    def transition_screen(self, new_screen_str, *args):
        self.current = new_screen_str
        Clock.schedule_once(partial(self.dismiss), 0.2)

    @mainthread
    def dismiss(self, *args):
        self.__dialog.dismiss()


class MainBoxNavigation(MDNavigationLayout):
    def __init__(self, **kwargs):
        super(MainBoxNavigation, self).__init__(**kwargs)


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        BeginConfiguration(self)

    def build(self):
        import os
        KV_DIR = '.'

        def builder_read(kv_file):
            with open(kv_file, encoding="utf-8") as kv:
                Builder.load_string(kv.read())

        def read_kv(KV_DIR):
            for kv_file in os.listdir(KV_DIR):
                kv_file = os.path.join(KV_DIR, kv_file)
                if os.path.isfile(kv_file):
                    name, test = os.path.splitext(kv_file)
                    if test == '.kv':
                        builder_read(kv_file)
                elif os.path.isdir(kv_file):
                    read_kv(kv_file)

        read_kv(KV_DIR)

        self.main_navigation = MainBoxNavigation()
        self.manager = self.main_navigation.manager

        return self.main_navigation


if __name__ in ('__main__', '__android__'):
    MainApp().run()
