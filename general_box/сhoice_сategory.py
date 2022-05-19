from kivymd.uix.gridlayout import MDGridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import CircularRippleBehavior, BackgroundColorBehavior
from kivy.uix.behaviors.button import ButtonBehavior
from utils.dispatcher import EventControl, GeneralColor


class HeaderBoxChoiceCategory(MDGridLayout):
    instance_box_category = []
    _active_box = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__class__.instance_box_category.append(self)

    def default_settings(self):
        for item in self.__class__.instance_box_category:
            if self == item:
                continue
            else:
                if EventControl.categories == 'costs':
                    instance = item.ids.costs
                    other = item.ids.income
                elif EventControl.categories == 'income':
                    instance = item.ids.income
                    other = item.ids.costs
                instance.text_color = GeneralColor.black
                other.text_color = GeneralColor.white
                self.line_color_update(instance, GeneralColor.black)
                self.line_color_delete(other)

    def choice_category(self, instance, manager):
        if self.__class__._active_box == instance:
            return
        if self.ids.income == instance:
            other = self.ids.costs
            EventControl.categories = 'income'
        elif self.ids.costs == instance:
            other = self.ids.income
            EventControl.categories = 'costs'

        instance.text_color = GeneralColor.black
        other.text_color = GeneralColor.white
        self.line_color_update(instance, GeneralColor.black)
        self.line_color_delete(other)

        if manager.current == 'MainScreen':
            manager.current_screen.set_data_for_query(category=EventControl.categories)

        self.default_settings()
        self.__class__._active_box = instance

    @staticmethod
    def line_color_update(instance, color):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(*color)
            RoundedRectangle(
                pos=(instance.pos[0], instance.pos[1] + 3),
                size=(instance.size[0], 3)
            )

    @staticmethod
    def line_color_delete(instance):
        instance.canvas.before.clear()

    @classmethod
    def overload_drow(cls):
        # FIXME не используемый метод
        if EventControl.categories == 'costs':
            instance = cls.instance_box_category[0].ids.costs
            other = cls.instance_box_category[0].ids.income
        elif EventControl.categories == 'income':
            instance = cls.instance_box_category[0].ids.income
            other = cls.instance_box_category[0].ids.costs

        instance.text_color = GeneralColor.black
        other.text_color = GeneralColor.white
        cls.line_color_update(instance, GeneralColor.black)
        cls.line_color_delete(other)

        cls._active_box = instance
        EventControl.categories = cls.category


class BoxForCheck(MDBoxLayout, CircularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    _active_check_box = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = ObjectProperty()
        # self._active_check_box = ObjectProperty()

    def choice_category(self, instance, manager):
        """Selecting an account, and writing to the dictionary of values from
        the database: category. """
        _check_list = instance.get_widgets(instance.group)
        if instance == self.__class__._active_check_box:
            instance.active = True
            return True
        for check in _check_list:
            if check != instance:
                check.active = False

        self.__class__._active_check_box = instance
        # self.check_active_box(instance)
        self.root.data_for_query.update({'category': self.category})
        # EventControl.categories = self.category
        # HeaderBoxChoiceCategory.overload_drow()
        if manager.current == 'AddArticleScreen':
            manager.current_screen.overload_icons()
