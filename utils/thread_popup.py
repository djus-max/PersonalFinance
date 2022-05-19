# -*- coding: utf-8 -*-
import concurrent.futures
from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock   # mainthread


class ContentPopup(BoxLayout):
    pass


class ThreadPopup():
    _flag = False

    def __init__(self, **kwargs):
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
        # self._flag = False

    def new_popup(self, inst_name_fun, **kwargs):
        """ Переход на скрин добавления перевода со скрина всех счетов"""
        if self.__class__._flag:
            inst_name_fun(**kwargs)
            return
        else:
            self.__class__._flag = True
            Clock.schedule_once(partial(self.__start_tread), 0)
            Clock.schedule_once(partial(self.__setting_new_parameters, inst_name_fun, **kwargs), 0.2)

    def __start_tread(self, dt, **kwargs):
        executor = concurrent.futures.ThreadPoolExecutor()
        f2 = executor.submit(self.__progress_popup)

    def __progress_popup(self):
        """ Добавление спинера загрузки в главный поток"""
        self.__dialog.open()

    def __setting_new_parameters(self, inst_name_fun, dt, **kwargs):
        """ настройка новых параметров нового окна"""
        inst_name_fun(**kwargs)
        Clock.schedule_once(partial(self.__dismiss), 0.2)

    # @mainthread
    def __dismiss(self, *args):
        self.__dialog.dismiss()
        self.__class__._flag = False
