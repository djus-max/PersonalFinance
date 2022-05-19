from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.utils import get_color_from_hex as hex
from kivymd.utils import asynckivy
from kivy.clock import Clock

# my module import
from general_box.box_icon import BoxForIcon, BoxForIconDetail
from general_box.header import Header
from utils.dispatcher import EventControl

from functools import partial


class HeaderAddIcon(Header):
    header_label = StringProperty('Выберите категорию')
    old_screen = ObjectProperty()
    old_screen_str = StringProperty('AddArticleScreen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_screen = EventControl.add_article_screen


class AddIconScreen(Screen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default_settings(self, **kwargs):
        self.ids.box_for_icon.adding_icons(
            flag_for_query=kwargs['flag_for_query'],
            data_for_query=kwargs['data_for_query'],
        )

    def default_settings_back(self):
        pass


class BoxForIconAddScreen(BoxForIcon):
    root_screen: ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BoxForIconAddScreen, self).__init__(**kwargs)
        # set padding
        number_of_icons = self._calculations_maximum_of_icons()

    def adding_icons(self, flag_for_query, data_for_query):        # TODO категория
        """Query the database and add icons. Sort by update date"""
        self.clear_widgets()
        # database query
        if flag_for_query == 'category':
            result = EventControl.database_outer.select_icon_for_add_screen(
                data_for_query['category'],
                selection=data_for_query['icon_group_id'],
            )
            self.root_screen.ids.header.header_label = 'Выберите категорию'
        if flag_for_query == 'group':
            result = EventControl.database_outer.select_icon_for_add_screen(
                data_for_query['category'],
                group=True,
            )
            self.root_screen.ids.header.header_label = 'Выберите группу'

        async def notify():
            for item in result:
                await asynckivy.sleep(0)
                box = BoxForIconDetailAddScreen(
                    icon_button=item.icon_name,
                    text_label=item.title,
                    color_icon=hex(item.icon_color),
                    id=item.id,
                )
                self.add_widget(box)
        asynckivy.start(notify())


class BoxForIconDetailAddScreen(BoxForIconDetail):
    """Icon selection and screen redirection"""
    def __init__(self, icon_button, text_label='', color_icon='', id='', **kwargs):
        super(BoxForIconDetailAddScreen, self).__init__(**kwargs)
        self.icon_button = icon_button
        self.text_label = text_label
        self.id = id
        self.ra, self.ga, self.ba, self.aa = list(color_icon)
        self._event = Clock.schedule_interval(partial(self.loading_content), 0.1)

    def category_selection(self, instance):
        if instance.icon == 'plus-thick':
            # self.add_widget(EventControl.manager_instance.screen_all_icon, index=0)
            EventControl.manager_instance.current = 'IconAllScreen'
            # EventControl.manager_instance.icon_all_screen()
        else:
            EventControl.database_outer.update_time_icons(self.id)
            EventControl.manager_instance.transition_article_screen_back()
