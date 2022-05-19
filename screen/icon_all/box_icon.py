from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty

# my modules
from utils.dispatcher import EventControl, GeneralColor
from general_box.box_icon import BoxIconCarousel, BoxForIcon, BoxForIconDetail    # ,BoxForCanvas, BoxIndex, BoxForCurrentIndex


##################################################################
# ############## Группа классов категории #########################


class BoxCategoryIconAll(MDBoxLayout):
    """  ids = box_category
            Отдельный класс для категорий с Label и каруселью"""
    root_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._info = {
            'box_for_icon': BoxForIconIconAll,
            'box_for_icon_detail': BoxForIconDetailIconAll,
            'root_box': self,
        }

    def build_icon(self, **kwargs):
        fun = self.set_icon
        EventControl.thread_popup().new_popup(fun, **kwargs)

    def set_icon(self, selection=None, flag=False, **kwargs):
        """ Запрос к базе данных с установелнными отборами, установка класса для иконок
            и передача в функцию установки"""
        self.default_settings()
        self._result_query = EventControl.database_inner.select_icon_all('category')
        self.ids.box_icon_carousel.build_icon(self._result_query, self._info)
        self.ids.box_for_canvas.build_canvas()

    def default_settings(self):
        self.ids.box_icon_carousel.clear_widgets()
        self.ids.label_text_icon.text_color = GeneralColor.text_color_global
        self.ids.box_icon_carousel.height = 0
        self.ids.box_index.clear_widgets()

    def default_settings_back(self):
        """ дефолтные настройки для цулого бокса """
        if self._info['box_for_icon_detail'].acive_icon:
            self._info['box_for_icon_detail'].acive_icon.ids.icon_button.md_bg_color = GeneralColor.grey
        self._info['box_for_icon_detail'].acive_icon = None
        self.ids.label_text_icon.text_color = GeneralColor.text_color_global
        self.ids.label_text_color.text_color = GeneralColor.text_color_global
        self.ids.box_icon_carousel.index = 0
        self.ids.box_icon_carousel.on_slide_complete()


class BoxIconCarouselIconAll(BoxIconCarousel):
    """ ids = box_icon_carousel"""
    root_box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BoxForIconIconAll(BoxForIcon):
    """ Класс бокса для добавления всех иконок категорий"""
    label_text_icon = ObjectProperty()

    def __init__(self, result, info, *args, **kwargs):
        super().__init__(result, info, *args, **kwargs)

    def _calculations_maximum_of_icons(self):
        width = Window.width * 0.9 * 0.95
        number_of_icons = int((width - 35) / (50 + 15))
        left_padding = ((width - 15) - ((50 + 15) * number_of_icons)) / 2
        self.padding = (left_padding, 0, 0, 10)
        return number_of_icons


class BoxForIconDetailIconAll(BoxForIconDetail):
    """ Класс для самих иконок категории"""

    def __init__(self, item, info, *args, **kwargs):
        super().__init__(item, info, *args, **kwargs)

    def begin_settings(self, item, info, *args, **kwargs):
        try:
            self.ids.icon_button.icon = item.name
            self.data = item
            self.info = info
        except Exception:
            self.disabled = True
            self.color_canvas_after = GeneralColor.dark_grey

    def set_active_icon(self):
        """ Установка активного экземляра и обновление данных для БД"""
        self.__class__.acive_icon = self
        self.info['root_box'].main_screen.data_for_query.update({'icon_name': self.data.name})
        self.info['root_box'].ids.label_text_icon.text_color = GeneralColor.text_color_global

    def category_selection(self, instance):
        """ Выбор иконки"""
        if self == self.__class__.acive_icon:
            return
        try:
            try:
                instance.md_bg_color = self.info['root_box'].main_screen.data_for_query['icon_color']
            except ValueError:
                instance.md_bg_color = GeneralColor.dark_grey
            finally:
                self.__class__.acive_icon.ids.icon_button.md_bg_color = GeneralColor.grey
        except AttributeError:
            pass
        finally:
            self.set_active_icon()


# ######################### Конец группы выбора категории #################
###########################################################################
