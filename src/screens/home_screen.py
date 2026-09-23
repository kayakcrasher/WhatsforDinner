"""
Home screen: user taps spin, animation plays, recipe appears.
"""

import random

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    """Main screen with the spin button and recipe result."""

    current_recipe = StringProperty("")
    is_spinning = BooleanProperty(False)

    def spin(self):
        """Kick off the spin animation and pick a recipe."""
        if self.is_spinning:
            return

        self.is_spinning = True
        self.current_recipe = ""

        self._start_spinner()
        Clock.schedule_once(self._reveal_recipe, 1.5)

    def _start_spinner(self):
        """Animate the SpinnerWidget's angle continuously."""
        spinner = self.ids.spinner
        spinner.opacity = 1

        anim = Animation(angle=360, d=1.0)
        anim.repeat = True
        anim.start(spinner)

    def _stop_spinner(self):
        """Stop the animation and hide the spinner."""
        spinner = self.ids.spinner
        Animation.cancel_all(spinner)
        spinner.opacity = 0

    def _reveal_recipe(self, dt):
        """Called after the spin delay. Picks a recipe and shows it."""
        self._stop_spinner()

        # Placeholder list. Will be replaced by the SQLite store.
        recipes = [
            "Spaghetti Bolognese",
            "Chicken Stir Fry",
            "Beef Tacos",
            "Vegetable Curry",
            "Grilled Salmon",
            "Margherita Pizza",
            "Pad Thai",
            "Shepherd's Pie",
        ]

        self.current_recipe = random.choice(recipes)
        self.is_spinning = False
