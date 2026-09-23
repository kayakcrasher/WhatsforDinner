"""Rounded button with soft shadow and press feedback."""

from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button

from src.utils import theme


class RoundedButton(Button):
    bg_color = ListProperty(list(theme.PRIMARY))
    bg_color_pressed = ListProperty(list(theme.PRIMARY_DARK))
    radius = NumericProperty(theme.RADIUS_PILL)
    shadow_alpha = NumericProperty(0.10)

    def on_state(self, *_):
        target = self.bg_color_pressed if self.state == "down" else self.bg_color
        Animation(bg_color=target, d=0.08).start(self)
