from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu

from general_box.header import Header
from utils.dispatcher import EventControl


class HeaderDetailArticle(Header):
    header_label = StringProperty('')

    def set_header_label(self, text):
        self.header_label = text


class DetailArticle(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        EventControl.detail_article_screen = self

        self.__class__.data_for_query = {
            'id_account': 0,
            'date': '',
            'id_article': '',
            'article_name': '',
        }

    def default_settings(self, **kwargs):
        try:
            if len(self.__class__.data_for_query['date']):
                result = EventControl.database_instance.select_detail_article_range(self.__class__.data_for_query)
        except TypeError:
            result = EventControl.database_instance.select_detail_article(self.__class__.data_for_query)
        summa = 0
        for item in result:
            summa += item[0].summa
        self.ids.header.set_header_label(f"{self.__class__.data_for_query['article_name']}\n{summa}")
        menu_items = [
            {
                "text": f"Item {i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            } for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            width_mult=4,
        )

    def default_settings_back(self):
        pass
