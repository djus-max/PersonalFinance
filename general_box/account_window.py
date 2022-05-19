from typing import Dict
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.properties import ListProperty, ObjectProperty
from kivymd.uix.behaviors import RectangularRippleBehavior, CircularRippleBehavior, BackgroundColorBehavior
from kivy.uix.behaviors.button import ButtonBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.list import TwoLineIconListItem

from functools import partial
from kivy.clock import Clock

from utils.dispatcher import EventControl, GeneralColor
from utils.re_text import division_of_amount
from collections import namedtuple


class BoxChoiceForAccount(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    """ Главный класс бокса выбора аккаунта """

    def build_item(self, row: Dict):
        """ Построение строчек счетов и передача главного класса экрана"""
        box = ItemConfirm(
            root=self,
            active=self.check_active(row.id),
            row=row,
        )
        self.items.append(box)

    def show_dialog_choice_account(self):
        result = EventControl.database_outer.select_account_info()
        self.items = []
        summa = 0

        for index, row in enumerate(result):
            self.build_item(row)
            summa += round(row.summa)
            if index == 0:
                currency_code = row.currency_code

        Row = namedtuple('row', 'id title summa currency_code icon_name icon_color ')
        row = Row(0, 'Всего', summa, currency_code, '', '#00000000')

        box_total = ItemConfirm(
            root=self,
            active=self.check_active(0),
            row=row
        )
        self.items.insert(0, box_total)
        self.dialog_add_open(self.items)

    def dialog_add_open(self, items):
        but = MDFlatButton(text="ОТМЕНА")
        self.dialog = WindowChoiceAccount(
            title="Выберите счет",
            type="confirmation",
            items=items,
            buttons=[
                but,
            ],
        )
        but.bind(on_release=self.dialog.dismiss)
        self.dialog.open()

    def check_active(self, id):
        if id == EventControl.manager_instance.current_screen.data_for_query['id_account']:
            return True
        return False


class BoxChoiceAccountMain(BoxChoiceForAccount):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        EventControl.choice_account_main = self

    def query_info_account(self):
        if EventControl.main_screen.data_for_query['id_account'] == 0:
            summa, currency_code = EventControl.database_outer.select_account_main_screen_total()
            Instance = namedtuple('instance', 'account_title summa currency_code id')
            instance = Instance('Всего', summa, currency_code, 0)

        else:
            account = EventControl.database_outer.select_account_main_screen(EventControl.main_screen.data_for_query['id_account'])
            Instance = namedtuple('instance', 'account_title summa currency_code id')
            instance = Instance(account.title, account.summa, account.currency_code, account.id)
        self.change_label(instance)

    def change_label(self, instance):
        self.ids.label_text_account.text = instance.account_title
        total_text = division_of_amount(int(instance.summa))
        self.ids.label_text_total.text = f"{str(total_text)} {instance.currency_code}"
        EventControl.main_screen.set_data_for_query(id_account=instance.id)


class BoxChoiceForAccountArticle(BoxChoiceForAccount):
    """ Бокс выбора счета на экране выбора статей расхода
        для дальнейшейго занесения в БД"""
    text_sign_money = ObjectProperty(None)

    def transition_settings(self, data):
        self.ids.label_text_account.text = data.title
        # self.ids.label_text_account.text_color = hex(data.out_account.icon_color)
        self.ids.icon_account.icon = data.icon_name
        self.ids.icon_account.text_color = hex(data.icon_color)
        self.text_sign_money.text = data.currency_code

    def show_dialog_choice_account(self):
        """ Выборка из БД всех счетов и открытие окна выбора"""
        result = EventControl.database_outer.select_account_info()
        self.items = []
        for row in result:
            self.build_item(row)
        self.dialog_add_open(self.items)

    def label_default(self):
        self.ids.label_text_account.text = 'Выберите счет'
        self.ids.label_text_account.text_color = GeneralColor.text_color_global
        self.ids.icon_account.icon = ''
        # self.ids.icon_account.text_color = instance.color_icon
        self.text_sign_money.text = ''

    def change_label(self, instance):
        """ Выбор счета.
            Изменения на экране.
            Занесение в словарь id счета для дальнейшей записи в БД."""

        self.ids.label_text_account.text = instance.account_title
        self.ids.label_text_account.text_color = GeneralColor.text_color_global
        self.ids.icon_account.icon = instance.icon
        self.ids.icon_account.text_color = instance.color_icon
        self.text_sign_money.text = f"  {instance.currency_code}"
        self.update_root_data_for_query(instance)

    def update_root_data_for_query(self, instance):
        EventControl.manager_instance.current_screen.data_for_query.update({
            'id_account': instance.id,
        })

    def change_label_error(self, *args, **kwargs):
        self.ids.label_text_account.text_color = GeneralColor.bright_red
        self.ids.label_text_account.wobble()


class BoxChoiceForAccountOutTransfer(BoxChoiceForAccountArticle):

    def build_item(self, row: Dict):
        """ Построение строчек счетов и передача главного класса экрана"""
        if self.checking_selected_account(row):
            super().build_item(row)
        else:
            return

    def checking_selected_account(self, row):
        if row.id == EventControl.manager_instance.current_screen.data_for_query['in_account_id']:
            return False
        else:
            return True

    def check_active(self, id):
        if id == EventControl.manager_instance.current_screen.data_for_query['out_account_id']:
            return True
        return False

    def update_root_data_for_query(self, instance):
        EventControl.manager_instance.current_screen.data_for_query.update({
            'out_account_id': instance.id,
        })

    def dialog_add_open(self, items):
        but_reset = MDFlatButton(
            text="СБРОСИТЬ",
            on_release=lambda but_reset: self.reset_account()
        )
        but = MDFlatButton(text="ОТМЕНА")
        self.dialog = WindowChoiceAccount(
            title="Выберите счет",
            type="confirmation",
            items=items,
            buttons=[
                but_reset,
                but,
            ],
        )
        but.bind(on_release=self.dialog.dismiss)
        self.dialog.open()

    def reset_account(self):
        EventControl.manager_instance.current_screen.data_for_query.update({
            'out_account_id': '',
        })
        self.label_default()
        self.dialog.dismiss()


class BoxChoiceForAccountInTransfer(BoxChoiceForAccountOutTransfer):

    def check_active(self, id):
        if id == EventControl.manager_instance.current_screen.data_for_query['in_account_id']:
            return True
        return False

    def update_root_data_for_query(self, instance):
        EventControl.manager_instance.current_screen.data_for_query.update({
            'in_account_id': instance.id,
        })

    def checking_selected_account(self, row):
        if row.id == EventControl.manager_instance.current_screen.data_for_query['out_account_id']:
            return False
        else:
            return True

    def reset_account(self):
        EventControl.manager_instance.current_screen.data_for_query.update({
            'in_account_id': '',
        })
        self.label_default()
        self.dialog.dismiss()

    def label_default(self):
        self.ids.label_text_account.text = 'Выберите счет'
        self.ids.label_text_account.text_color = GeneralColor.text_color_global
        self.ids.icon_account.icon = ''
        # self.ids.icon_account.text_color = instance.color_icon

    def change_label(self, instance):
        """ Выбор счета.
            Изменения на экране.
            Занесение в словарь id счета для дальнейшей записи в БД."""

        self.ids.label_text_account.text = instance.account_title
        self.ids.label_text_account.text_color = GeneralColor.text_color_global
        self.ids.icon_account.icon = instance.icon
        self.ids.icon_account.text_color = instance.color_icon
        self.update_root_data_for_query(instance)


class BoxChoiceAccountDetail(BoxChoiceForAccount):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ItemConfirm(TwoLineIconListItem, CircularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    """ Строки выбора счета"""
    divider = None

    def __init__(self, root, active, row, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.active = active

        # Инициализация переменных для дальнейшей обработки
        self.id = row.id
        self.account_title = row.title
        self.summa = round(row.summa)
        self.currency_code = row.currency_code
        self.icon = self.ids.icon.icon = row.icon_name
        self.color_icon = self.ids.icon.md_bg_color = hex(row.icon_color)

        # Обработки текста и вывод на экран
        total_text = division_of_amount(row.summa)
        title = row.title if len(row.title) < 10 else f"{row.title[:10]}..."
        # title = f"[color={get_hex_from_color(GeneralColor.bright_red)}]{title}[/color]"
        self.text = f"{str(total_text)} [color=ff0000]{row.currency_code}[/color]"
        self.secondary_text = title
        self.check = Check(active=active)
        self.add_widget(self.check)

    def press_choice_account(self):
        """Selecting an account, and writing to the dictionary of values from
        the database: id, account. """
        if self.active:
            self.check.active = True
        self.root.change_label(self)
        Clock.schedule_once(partial(self.root.dialog.dismiss), 0.3)


class Check(MDCheckbox):
    def __init__(self, active, **kwargs,):
        super().__init__(**kwargs)
        self.active = active


class WindowChoiceAccount(MDDialog):
    md_bg_color = GeneralColor.white
