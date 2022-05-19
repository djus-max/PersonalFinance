from kivy.properties import ObjectProperty, DictProperty
from kivy.utils import get_color_from_hex as hex


class GeneralColor:
    white = hex('#ffffffff')
    black = hex('#000000ff')
    grey = hex('#cececeff')
    bright_red = hex('#ff0000ff')
    bright_blue = hex('#0000ffff')
    bright_green = hex('#00ff00ff')
    bright_yellow = hex('#ffff00ff')
    ligtly_blue = hex('#00ffffff')
    violet = hex('#ff00e6ff')
    ligtly_green = hex('#98c989ff')
    dark_grey = hex('#574e4eff')
    colorless = hex('#00000000')
    header_color = bright_green
    icon_inner_color = white
    text_color_global = black


class EventControl():
    main_screen = ObjectProperty(None)                # TODO remove on_touch_move
    add_account_screen = ObjectProperty(None)
    add_article_screen = ObjectProperty(None)
    add_icon_screen = ObjectProperty(None)
    icon_all_screen = ObjectProperty(None)
    all_account_screen = ObjectProperty(None)
    add_transfer_screen = ObjectProperty(None)
    # detail_article_screen = ObjectProperty()
    choice_account_main = ObjectProperty(None)  # класс выбора счета на главном экране
    header_main = ObjectProperty(None)
    # Database instance
    database_inner = ObjectProperty(None)
    database_outer = ObjectProperty(None)
    manager_instance = ObjectProperty(None)
    thread_popup = ObjectProperty(None)
    # Боковая панель
    navigationBar = ObjectProperty(None)
    categories = 'costs'
    detail_data_for_query = {}

    def __setattr__(self, key, value):
        setattr(self.__class__, key, value)
        if key == 'categories':
            # self.__class__.add_article_screen.data_for_query.update({
            # 'category': value})
            self.__class__.main_screen.data_for_query.update({'category': value})
