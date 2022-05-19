import os
from kivy.core.window import Window
from kivy.config import Config
from kivy.cache import Cache
from kivy.properties import StringProperty

from utils.dispatcher import EventControl
from database.manage_inner import ManageBaseInner
from database.manage_outer import ManageBaseOuter
from utils.thread_popup import ThreadPopup


class BeginConfiguration():
    """
    класс создания внутренних дерикторий приложежния, насроек и базы данных для
    сохранения точек передвижения.
    """
    _os_platform = StringProperty('')
    _app_dir = StringProperty('')
    cache_name = 'mycache'

    @classmethod
    def __init__(cls, my_app):
        cls.cache_name = 'mycache'
        cls.my_app = my_app
        cls.check_platform()
        cls.check_folder()
        EventControl.thread_popup = ThreadPopup
        data_dir = str(os.path.join(cls._app_dir, 'data/config.ini'))
        Config.read(data_dir)
        Cache.register(cls.cache_name)
        cls.config_file_set('kivy', 'log_maxfiles', '10')
        Config.setdefaults(
            'mydata', {
                'flag': 1,
            }
        )
        Config.write()
        cls.create_data_base()   # TODO ADD PATH APP
        cls.my_app.theme_cls.theme_style = "Light"  # "Light"  "Dark"
        Window.softinput_mode = "below_target"

    @classmethod
    def config_file_get(cls, *args):
        arg = args
        return Config.get(arg[0], arg[1])

    @classmethod
    def config_file_set(cls, *args):
        arg = args
        Config.set(arg[0], arg[1], arg[2])
        Config.write()

    @classmethod
    def check_platform(cls):
        """ Проверка ОС.
        При удачном импортироании  cls._os_platform = 'android',
        иначе cls._os_platform = 'linux'.
        Так же присваиваеться путь приложения."""
        try:
            from android.storage import primary_external_storage_path
            from jnius import autoclass, PythonJavaClass, java_method
            # Environment = autoclass('android.os.Environment')
            context = autoclass('android.content.Context')
            path_file = context.getExternalFilesDir(None)
            path = path_file.getAbsolutePath()
            cls._os_platform = 'android'
            cls._app_dir = path

        except ImportError:
            cls._os_platform = 'linux'
            cls._app_dir = os.getcwd()
            Window.size = (400, 580)

    @classmethod
    def check_folder(cls):
        ''' проверка и создание каталага для логов приложения в директории памяти '''
        dir_save_log = str(os.path.join(cls._app_dir, 'data/logs'))
        check_dir_save_log = os.path.exists(dir_save_log)
        if not check_dir_save_log:
            os.mkdir(dir_save_log, mode=0o777)
        flag_logs = BeginConfiguration.config_file_get('kivy', 'log_dir')
        if flag_logs != dir_save_log:
            BeginConfiguration.config_file_set('kivy', 'log_name', 'finance_%y-%m-%d_%_.txt')
            BeginConfiguration.config_file_set('kivy', 'log_dir', dir_save_log)

    @classmethod
    def create_data_base(cls):
        data_base_inner = ManageBaseInner(os.path.join(cls._app_dir, 'data/DataBaseInner.db'))
        EventControl.database_inner = data_base_inner
        data_base_outer = ManageBaseOuter(os.path.join(cls._app_dir, 'data/DataBaseOuter.db'))
        EventControl.database_outer = data_base_outer
