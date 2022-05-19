from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior
from kivy.uix.behaviors.button import ButtonBehavior
from kivymd.uix.list import TwoLineAvatarListItem
from kivymd.uix.dialog import MDDialog

# my module import
from utils.dispatcher import EventControl, GeneralColor
from general_box.header import Header


class HeaderAddAccount(Header):
    """ шапка экрана с предопределенной надписью"""
    header_label = StringProperty('Создайте счет')


class BoxCurrency(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    """ Бокс надписи и выбора валюты"""
    text_currency = ObjectProperty(None)    # Текст надписи на экране

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Запрос к базе даннх на все валюты
        self.result_query = EventControl.database_inner.select_сurrency_all()

    def box_choice_currency(self):
        """ Обработчик нажатия для выбора валюты списком"""
        items = []
        for item in self.result_query:
            box = ItemConfirmCurrency(
                item,
                text=f"{item.name}    {item.sign}",
                secondary_text=item.code,
            )
            items.append(box)
            box.bind(on_release=self.choice_currency)
        self.dialog = ChoiceCurrency(
            title="Выберите Валюту",
            type="confirmation",
            items=items,
        )
        self.dialog.open()

    def choice_currency(self, instance):
        """ Выбор валюты, вывод на экран и передача в словарь для дальнейшего занесения в базу"""
        self.text_currency.text = f'  {instance.secondary_text}    {instance.sign}'
        EventControl.add_account_screen.data_for_query.update({
                    'currency_name': instance.name,
                    'currency_code': instance.code,
                    'currency_sign': instance.sign,
        })
        self.text_currency.text_color = GeneralColor.text_color_global
        self.dialog.dismiss()


class ChoiceCurrency(MDDialog):
    md_bg_color = GeneralColor.white


class ItemConfirmCurrency(TwoLineAvatarListItem, ButtonBehavior, BackgroundColorBehavior):
    ''' Объект строчек выбора валюты.
        Обработчик события выбора привязан в вызывающем классе '''
    def __init__(self, item, **kwargs):
        super().__init__(**kwargs)
        self.name = item.name
        self.code = item.code
        self.sign = item.sign


class AddAccountScreen(Screen):
    ''' Экран добавления счета'''
    main_self = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__class__.main_self = self
        EventControl.add_account_screen = self
        # Запрос к к внутренней базе
        result_query = EventControl.database_inner.select_icon_all('account')   # FIXME
        # Вызов построения иконок BoxChangeAccountScreen(general_box.box_icon.BoxChange)
        # self.ids.box_change.build_icon(self, result_query)
        self.default_settings()
        self.ids.box_category.build_icon()

    def default_settings(self, **kwargs):
        ''' Дефолтные данне необходимые для базы данных '''
        self.data_for_query = {
                'title': '',
                'summa': '',
                'icon_name': '',
                'icon_color': '',
                'currency_name': '',
                'currency_code': '',
                'currency_sign': '',
                'main': False,
        }

    def default_settings_back(self):
        """default screen settings"""
        pass

    def query_insert_icon(self):
        """Validating all required fields and submitting data to the database"""
        if self.data_for_query['summa'] == '':
            self.ids.text_field_summa.error = True
            self.ids.text_field_summa.focus = True
            self.ids.text_field_summa.helper_text = 'Введите сумму'
            return
        elif self.data_for_query['currency_name'] == '':
            self.ids.text_currency.text_color = GeneralColor.bright_red
            self.ids.text_currency.wobble()
            return
        elif self.data_for_query['title'] == '':
            self.ids.text_category.error = True
            self.ids.text_category.focus = True
            self.ids.text_category.helper_text = 'Введите название'
            return
        elif self.data_for_query['icon_name'] == '':
            self.ids.box_category.ids.label_text_icon.text_color = GeneralColor.bright_red
            self.ids.box_category.ids.label_text_icon.wobble()
            return
        elif self.data_for_query['icon_color'] == '':
            self.ids.box_category.ids.label_text_color.text_color = GeneralColor.bright_red
            self.ids.box_category.ids.label_text_color.wobble()
            return
        else:
            EventControl.database_outer.query_insert_account(self.data_for_query)
            EventControl.manager_instance.new_screen_transition(EventControl.main_screen, "MainScreen", 'default')
