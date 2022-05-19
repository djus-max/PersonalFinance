from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors.elevation import FakeRectangularElevationBehavior
from kivy.properties import ListProperty, StringProperty
from kivy.utils import get_color_from_hex


class BoxDetail(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior, FakeRectangularElevationBehavior):
    ripple_scale = 0.7
    icon = StringProperty()
    icon_color_bg = ListProperty([0, 0, 0, 0])
    article_name = StringProperty()
    percent = StringProperty()
    score = StringProperty()


class AccountBox(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_article(self, result):
        self.clear_widgets()
        for item in result:
            box = AccountBoxDetail(item,)
            self.add_widget(box)


class AccountBoxDetail(BoxDetail):

    def __init__(self, item, **kwargs):
        super().__init__(**kwargs)
        self.ids.first_label.icon = item.icon_name
        self.ids.first_label.md_bg_color = get_color_from_hex(item.icon_color)
        self.ids.second_label.text = item.title
        self.ids.third_label.text = f"{str(item.summa)}  [color=ff0000]{item.currency_code}[/color]"
        self.data = item


class TransferBox(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_article(self, result):
        self.clear_widgets()
        for item in result:
            box = TransferBoxDetail(item)
            self.add_widget(box)


class TransferBoxDetail(BoxDetail):

    def __init__(self, item, **kwargs):
        super().__init__(**kwargs)

        self.ids.date_label.text = item.date.strftime("%-d.%m")
        self.ids.first_label.icon = item.out_account.icon_name
        self.ids.first_label.text_color = get_color_from_hex(item.out_account.icon_color)
        self.ids.second_label.text = item.out_account.title
        self.ids.fourth_label.icon = item.in_account.icon_name
        self.ids.fourth_label.text_color = get_color_from_hex(item.in_account.icon_color)
        self.ids.fifth_label.text = item.in_account.title
        self.ids.sixth_label.text = f"{str(item.summa)}  [color=ff0000]{item.out_account.currency_sign}[/color]"
        self.data = item
