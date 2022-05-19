from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from general_box.box_data import BoxForDataDetailTransfer

# my module import
from utils.dispatcher import EventControl, GeneralColor
from general_box.header import Header


class HeaderAddTransfer(Header):
    """ Шапка экрана"""
    header_label = StringProperty('Перевод на другой счет')
    old_screen = ObjectProperty()
    old_screen_str = StringProperty('AllAccountScreen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_screen = EventControl.all_account_screen


class AddTransferScreen(Screen):
    """ Экран добавления перевода"""
    box_change = ObjectProperty()
    box_save = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        EventControl.add_transfer_screen = self
        self.data_for_query = {}
        self.begin_settings()

    def begin_settings(self):
        # построение дат
        self.ids.box_for_data.build_box()
        self.default_settings_data()

    def default_settings_data(self):
        self.data_for_query = {
            'id': '',
            'date': '',
            'out_account_id': '',
            'in_account_id': '',
            'summa': '',
            'comment': '',
        }

    def default_settings(self, **kwargs):
        self.ids.box_choice_for_out_account.label_default()
        self.ids.box_choice_for_in_account.label_default()
        BoxForDataDetailTransfer.default_settings()
        self.clear_text_label()
        self.ids.label_text_data.text_color = GeneralColor.text_color_global
        self.default_settings_data()
        self.ids.box_change.size_hint = (0, 0)
        self.ids.box_save.size_hint = (1, 1)
        self.ids.box_change.opacity = 0
        self.ids.box_change.disabled = True
        self.ids.box_save.opacity = 1
        self.ids.box_save.disabled = False
        self.ids.button_save.md_bg_color = GeneralColor.header_color

    def old_settings(self, **kwargs):
        data = kwargs['data_for_query']
        self.data_for_query.update({
            'id': data.id,
            'date': data.date,
            'out_account_id': data.out_account_id,
            'in_account_id': data.in_account_id,
            'summa': data.summa,
            'comment': data.comment,
        })

        self.ids.text_field_summa.text = str(data.summa)
        self.ids.text_field_comment.text = str(data.comment)
        self.ids.box_choice_for_out_account.transition_settings(data.out_account)
        self.ids.box_choice_for_in_account.transition_settings(data.in_account)
        BoxForDataDetailTransfer.transition_settings(data.date)
        self.ids.box_save.opacity = 0
        self.ids.box_save.disabled = True
        self.ids.box_change.opacity = 1
        self.ids.box_change.disabled = False
        self.ids.button_change.md_bg_color = GeneralColor.header_color
        self.ids.button_delete.md_bg_color = GeneralColor.bright_red
        self.ids.box_save.size_hint = (0, 0)
        self.ids.box_change.size_hint = (1, 1)

    def default_settings_back(self):
        # в любом случае
        # self.default_settings_data()
        self.ids.box_choice_for_out_account.label_default()
        self.ids.box_choice_for_in_account.label_default()
        BoxForDataDetailTransfer.default_settings()
        self.clear_text_label()
        self.ids.label_text_data.text_color = GeneralColor.text_color_global
        self.default_settings_data()

    def clear_text_label(self):
        self.ids.text_field_summa.text = ''
        self.ids.text_field_comment.text = ''

    def query_insert_transfer(self):
        """Validating all required fields and submitting data to the database"""
        if self.data_for_query['summa'] == '':
            # self.ids.scroll_box.scroll_y = 1
            self.ids.text_field_summa.error = True
            self.ids.text_field_summa.focus = True
            return
        elif self.data_for_query['out_account_id'] == '':
            # self.ids.box_choice_for_account.ids.label_text_account.text_color = GeneralColor.bright_red
            # self.ids.box_choice_for_account.ids.label_text_account.wobble()
            self.ids.box_choice_for_out_account.change_label_error()
            return
        elif self.data_for_query['in_account_id'] == '':
            # self.ids.box_choice_for_account.ids.label_text_account.text_color = GeneralColor.bright_red
            # self.ids.box_choice_for_account.ids.label_text_account.wobble()
            self.ids.box_choice_for_in_account.change_label_error()
            return
        elif self.data_for_query['date'] == '':
            self.ids.label_text_data.text_color = GeneralColor.bright_red
            self.ids.label_text_data.wobble()
            return

        # Запись в БД перевода
        EventControl.database_outer.query_insert_transfer(self.data_for_query)
        EventControl.manager_instance.new_screen_transition(EventControl.all_account_screen,
                                                            "AllAccountScreen",
                                                            'default',
                                                            )

    def query_update_transfer(self):
        EventControl.database_outer.query_update_transfer(self.data_for_query)
        EventControl.manager_instance.new_screen_transition(EventControl.all_account_screen,
                                                            "AllAccountScreen",
                                                            'default',
                                                            )

    def query_delete_transfer(self):
        EventControl.database_outer.query_delete_transfer(self.data_for_query)
        EventControl.manager_instance.new_screen_transition(EventControl.all_account_screen,
                                                            "AllAccountScreen",
                                                            'default',
                                                            )
