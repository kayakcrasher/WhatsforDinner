"""Soft card container with rounded corners and shadow."""

from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

from src.utils import theme


class Card(BoxLayout):
    bg_color = ListProperty(list(theme.SURFACE))
    radius = NumericProperty(theme.RADIUS_LG)
    shadow_alpha = NumericProperty(0.05)
