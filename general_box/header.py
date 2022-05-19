from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import ListProperty
from utils.dispatcher import GeneralColor
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.elevation import FakeRectangularElevationBehavior


class Header(MDGridLayout):
    color_header_canvas = ListProperty(GeneralColor.header_color)
    pass


class CentrWidget(MDBoxLayout, FakeRectangularElevationBehavior):
    color_canvas = ListProperty(GeneralColor.white)
