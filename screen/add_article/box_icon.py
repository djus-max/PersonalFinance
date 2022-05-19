from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import CircularRippleBehavior, BackgroundColorBehavior
from kivy.uix.behaviors.button import ButtonBehavior
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.properties import ObjectProperty

# my modules
from utils.dispatcher import EventControl, GeneralColor
from general_box.box_icon import BoxIconCarousel, BoxForIcon, BoxForIconDetail    # ,BoxForCanvas, BoxIndex, BoxForCurrentIndex

import math

##################################################################
# ############## Группа классов категории #########################


class BoxCategoryArticle(MDBoxLayout):
    """  ids = box_category
            Отдельный класс для категорий с Label и каруселью"""
    root_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._info = {
            'flag_icon_active': False,
            'box_for_icon': BoxForIconArticleCategory,
            'box_for_icon_detail': BoxForIconDetailArticleCategory,
            'root_box': self,
        }
        self.button_plus_article = ButtonPlusArticle()

    def build_icon(self, flag=False, **kwargs):
        self._info.update({'flag_icon_active': flag})
        fun = self.set_icon
        EventControl.thread_popup().new_popup(fun, **kwargs)

    def set_icon(self, selection=None, **kwargs):
        """ Запрос к базе данных с установелнными отборами, установка класса для иконок
            и передача в функцию установки"""
        category = self.root_screen.data_for_query['category']
        # self._result_query = EventControl.database_inner.select_icon_all('category')
        self.default_settings()
        self._result_query = EventControl.database_outer.select_icon_for_add_screen(category=category, selection=selection)
        self.ids.box_icon_carousel.build_icon(self._result_query, self._info)
        # TODO Кнопка перехода экрана - динамическая
        self.add_widget(self.button_plus_article)

    def default_settings(self):
        self.ids.box_icon_carousel.clear_widgets()
        self.ids.label_text_icon.text_color = GeneralColor.text_color_global
        self.ids.box_icon_carousel.height = 0
        self.ids.box_index.clear_widgets()
        if self.button_plus_article:
            self.remove_widget(self.button_plus_article)


class BoxIconCarouselArticle(BoxIconCarousel):
    """ ids = box_icon_carousel"""
    root_box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _count_carousel(self, length: int, multi_size_hint_x, sum_padding_left_right) -> int:
        """Counting the icons that fit in the window.
        Entering into the general variable the number of icons in two rows.
        """
        _width = Window.width * multi_size_hint_x
        number_of_icons = int((_width - sum_padding_left_right) / (50 + 15))
        number = math.ceil(length / (number_of_icons * 2 - 1))
        return number_of_icons * 2 - 1, number


class BoxForIconArticleCategory(BoxForIcon):
    """ Класс бокса для добавления всех иконок категорий"""
    label_text_icon = ObjectProperty()

    def __init__(self, result, info, *args, **kwargs):
        super().__init__(result, info, *args, **kwargs)


class BoxForIconDetailArticleCategory(BoxForIconDetail):
    """ Класс для самих иконок категории"""

    def __init__(self, item, info, *args, **kwargs):
        super().__init__(item, info, *args, **kwargs)

    def begin_settings(self, item, info, *args, **kwargs):
        try:
            self.ids.icon_button.icon = item.icon_name
            self.ids.label.text = item.title
            self.data = item
            self.info = info
            self.click_icon_color = item.icon_color
            self.id = item.id
            self.ids.icon_button.tooltip_text = item.title
            if info['flag_icon_active']:
                self.ids.icon_button.md_bg_color = item.icon_color
                self.__class__.acive_icon = self
                info['root_box']._info.update({'flag_icon_active': False})
        except Exception:
            self.disabled = True
            self.color_canvas_after = GeneralColor.white

    def set_active_icon(self):
        """ Установка активного экземляра и обновление данных для БД"""
        self.__class__.acive_icon = self
        EventControl.add_article_screen.data_for_query.update({'icon_category_id': self.id})
        self.info['root_box'].ids.label_text_icon.text_color = GeneralColor.text_color_global

    def category_selection(self, instance):
        """ Выбор иконки"""
        if self == self.acive_icon:
            return
        elif self != self.__class__.acive_icon:
            instance.md_bg_color = self.click_icon_color
        try:
            self.__class__.acive_icon.ids.icon_button.md_bg_color = GeneralColor.grey
        except AttributeError:
            pass
        finally:
            self.set_active_icon()


class ButtonPlusArticle(MDRelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# ########## Конец группы выбора категории ################
###########################################################


###########################################################
# #### Группа классов выбора  категории группы группы ######


class BoxGroupArticle(MDBoxLayout):
    """ ids = box_category"""
    root_screen = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._info = {
            'flag_icon_active': False,
            'box_for_icon': BoxForIconArticleGroup,
            'box_for_icon_detail': BoxForIconDetailArticleGroup,
            'root_box': self,
        }
        self.button_plus_group = ButtonPlusGroup()

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.ids.label_text_icon.text_color = GeneralColor.black
            self.ids.icon_chevron_group.icon = 'chevron-down'
            self.ids.icon_chevron_group.text_color = GeneralColor.black
            EventControl.add_article_screen.ids.box_category.default_settings()
            self.build_icon()
            EventControl.add_article_screen.data_for_query.update({
                'icon_group_id': None,
                'icon_category_id': None,
            })
        else:
            self.default_settings_box()
            EventControl.add_article_screen.data_for_query.update({
                'icon_group_id': None,
                'icon_category_id': None,
            })
            EventControl.add_article_screen.ids.box_category.build_icon()

    def build_icon(self, flag=False, **kwargs):
        self._info.update({'flag_icon_active': flag})
        fun = self.set_icon
        EventControl.thread_popup().new_popup(fun, **kwargs)

    def set_icon(self):
        """ Запрос к базе данных с установелнными отборами, установка класса для иконок
            и передача в функцию установки"""
        category = self.root_screen.data_for_query['category']
        # self._result_query = EventControl.database_inner.select_icon_all('category')
        self.default_settings()
        self._result_query = EventControl.database_outer.select_icon_for_add_screen(category=category, group=True)
        self.ids.box_icon_carousel.build_icon(self._result_query, self._info)
        # TODO Кнопка перехода экрана - динамическая
        self.add_widget(self.button_plus_group)

    def default_settings(self):
        self.ids.box_icon_carousel.clear_widgets()
        self.ids.label_text_icon.text_color = GeneralColor.text_color_global
        self.ids.box_icon_carousel.height = 0
        self.ids.box_index.clear_widgets()
        if self.button_plus_group:
            self.remove_widget(self.button_plus_group)

    def default_settings_box(self):
        self.ids.label_text_icon.text_color = GeneralColor.dark_grey
        self.ids.icon_chevron_group.icon = 'chevron-right'
        self.ids.icon_chevron_group.text_color = GeneralColor.dark_grey
        self.ids.check_group.active = False
        self.ids.box_icon_carousel.clear_widgets()
        self.ids.box_icon_carousel.height = 0
        self.ids.box_index.clear_widgets()
        self.remove_widget(self.button_plus_group)


class BoxIconCarouselGroup(BoxIconCarouselArticle):
    """ box_icon_carousel"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BoxForIconArticleGroup(BoxForIconArticleCategory):
    """ Класс бокса для группы-категории для добавления всех иконок категорий"""
    label_text_icon = ObjectProperty()

    def __init__(self, result, info, *args, **kwargs):
        super().__init__(result, info, *args, **kwargs)


class BoxForIconDetailArticleGroup(BoxForIconDetailArticleCategory):
    """ Класс для самих иконок группы-категории"""
    def __init__(self, item, info, *args, **kwargs):
        super().__init__(item, info, *args, **kwargs)

    def set_active_icon(self):
        """ Установка активного экземляра и обновление данных для БД"""
        self.__class__.acive_icon = self
        EventControl.add_article_screen.data_for_query.update({
            'icon_group_id': self.id,
            'icon_category_id': None,
        })
        EventControl.add_article_screen.ids.box_category.build_icon(selection=self.id)
        self.info['root_box'].ids.label_text_icon.text_color = GeneralColor.text_color_global


class ButtonAddGroup(MDBoxLayout, CircularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ButtonPlusGroup(MDRelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# ######################### Конец категории группы #####################
#######################################################################
