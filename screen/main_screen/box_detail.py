from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors.elevation import FakeRectangularElevationBehavior
from kivy.properties import StringProperty, ObjectProperty
from kivy.utils import get_color_from_hex

# my modules
from utils.dispatcher import EventControl, GeneralColor
from utils.re_text import division_of_amount


class ArticleBox(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_article(self, result, summa):
        list_article = []
        self.clear_widgets()
        for item in result:
            percent = round(item.total / summa * 100, 2)
            if item[1].icon_group:
                icon_color_bg = get_color_from_hex(item[1].icon_group.icon_color)
                list_article.append((icon_color_bg, percent))
            elif item[1].icon_group is None:
                icon_color_bg = get_color_from_hex(item[1].icon_category.icon_color)
                list_article.append((icon_color_bg, percent))
            percent = round(percent)
            box = ArticleBoxDetail(
                item=item[1],
                summa=item.total,
                percent=percent,
            )
            self.add_widget(box)
        return list_article


class ArticleBoxDetail(MDBoxLayout, BackgroundColorBehavior, FakeRectangularElevationBehavior):

    def __init__(self, item, summa, percent, **kwargs):
        super().__init__(**kwargs)
        box = ArticleBoxGroup(
            item=item,
            summa=summa,
            percent=percent,
            root_box=self,
        )
        self.add_widget(box)

    def set_article_detail_group(self, result, summa):
        list_article = []
        for item in result:
            percent = round(item.total / summa * 100, 2)
            icon_color_bg = get_color_from_hex(item[1].icon_category.icon_color)
            list_article.append((icon_color_bg, percent))
            percent = round(percent)
            box = ArticleBoxGroupDetail(
                item=item[1],
                summa=item.total,
                percent=percent,
                root_box=self
            )
            self.add_widget(box)

    def delete_article_detail_group(self):
        for child in self.children[:-1]:
            self.remove_widget(child)


class ArticleBoxGroup(MDBoxLayout):
    _flag_category = StringProperty(None)
    _root_box = ObjectProperty(None)
    _flag_detail = False

    def __init__(self, item, summa, percent, root_box, **kwargs):
        super().__init__(**kwargs)
        self._root_box = root_box
        self._summa = summa
        summa = division_of_amount(summa)
        self.id = item.id
        self.ids.third_label.text = f'{percent} %'
        self.ids.fourth_label.text = f" {str(summa)} [color=ff0000] {item.account.currency_sign} [/color]"
        if item.icon_group:
            self.ids.first_label.icon = item.icon_group.icon_name
            self.article_name = item.icon_group.title
            self.ids.second_label.text = self.article_name
            self.ids.first_label.md_bg_color = get_color_from_hex(item.icon_group.icon_color)
            self._flag_category = 'group'
            # TODO цвет кнопки расширения и разрешения нажимать
            self.ids.label_button.icon = 'chevron-right'
            self.ids.label_button.text_color = GeneralColor.black
            self.ids.label_button.disabled = False
            self.ids.label_button.ripple_scale = 1
        elif item.icon_group is None:
            self.ids.first_label.icon = item.icon_category.icon_name
            self.article_name = item.icon_category.title
            self.ids.second_label.text = self.article_name
            self.ids.first_label.md_bg_color = get_color_from_hex(item.icon_category.icon_color)
            self._flag_category = 'category'
        self.data = item

    def general_press(self):
        pass

    def button_press(self):
        if self._flag_category == 'group':
            if not self._flag_detail:
                EventControl.main_screen.query_detail_data(
                        instance=self._root_box,
                        icon_group_id=self.data.icon_group_id
                )
                self._flag_detail = True
                self.ids.label_button.icon = 'chevron-down'
            elif self._flag_detail:
                # отчистить виджет
                self._root_box.delete_article_detail_group()
                self._flag_detail = False
                self.ids.label_button.icon = 'chevron-right'


class ArticleBoxGroupDetail(MDBoxLayout):
    _flag_category = StringProperty(None)
    _root_box = ObjectProperty(None)
    _flag_detail = False

    def __init__(self, item, summa, percent, root_box, **kwargs):
        super().__init__(**kwargs)
        self._root_box = root_box
        self._summa = summa
        summa = division_of_amount(summa)
        self.id = item.id
        self.ids.third_label.text = f'{percent} %'
        self.ids.fourth_label.text = f" {str(summa)} [color=ff0000] {item.account.currency_sign} [/color]"
        self.ids.first_label.icon = item.icon_category.icon_name
        self.article_name = item.icon_category.title
        self.ids.second_label.text = self.article_name
        self.ids.first_label.text_color = get_color_from_hex(item.icon_category.icon_color)
        self._flag_category = 'category'
        self.data = item

    def general_press(self):
        pass


class ArticleBoxDetailButton(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    pass
