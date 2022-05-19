from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from utils.dispatcher import EventControl


class ItemDrawer(OneLineIconListItem):
    """ Класс строчки в списке"""
    icon = StringProperty()

    def __init__(self, screen, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen


class ContentNavigationDrawer(MDBoxLayout):
    """ Класс контента входящего в боковую панель"""
    navigation_bar = ObjectProperty()


class DrawerList(ThemableBehavior, MDList):
    """ Класс динамического  отображения списка"""

    def transition_screen(self, instance_item, app):
        ''' Called when tap on a menu item. '''
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
        app.manager.transition_all_account_screen(instance_item.screen)
        EventControl.navigationBar.set_state('toggle')


class NavigationBar(MDNavigationDrawer):
    """ Класс боковой панели"""
    content_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        EventControl.navigationBar = self

    def on_start(self):
        """ открытие боковой панели с добавлением строчек выбора"""
        self.set_state('toggle')
        screen_item = [
                ["MainScreen", {"home": "Главная"}],
                ["AllAccountScreen", {"account": "Счета"}, ],
        ]

        self.content_drawer.ids.md_list.clear_widgets()
        for item in screen_item:
            for icon_name in item[1].keys():
                self.content_drawer.ids.md_list.add_widget(
                    ItemDrawer(
                        screen=item[0],
                        icon=icon_name,
                        text=item[1][icon_name],
                    )
                )
