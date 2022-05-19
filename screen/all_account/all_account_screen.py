from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout

# my modules
from utils.dispatcher import EventControl
from general_box.header import Header


class HeaderAllAccount(Header):
    header_label = StringProperty('Счета')


class Tab(MDBoxLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class AllAccountScreen(Screen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        EventControl.all_account_screen = self

    def begin_settings(self):
        pass

    def default_settings(self, **kwargs):
        self.ids.tabs.switch_tab("Все счета")
        account_result = EventControl.database_outer.select_account_info()
        self.ids.tabAccount.ids.article_box.set_article(account_result)
        transfer_result = EventControl.database_outer.select_transfer_info()
        self.ids.tabTransfer.ids.article_box.set_article(transfer_result)

    def default_settings_back(self):
        # self.ids.tabs.switch_tab("Все счета")
        pass

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text, *args):
        '''Called when switching tabs.
        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        # instance_tab.ids.label.text = tab_text
        pass
