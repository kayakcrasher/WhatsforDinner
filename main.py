"""
What's for Dinner - Application entry point.

Imports screens from src/, registers resource paths,
loads KV files, builds the ScreenManager.
"""

import os

from kivy.app import App
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager

# Import screens and widgets so Kivy's Factory knows about them
# BEFORE the KV file is loaded. The noqa comments silence "unused import"
# warnings from linters -- these imports register classes as a side effect.
from src.screens.home_screen import HomeScreen  # noqa: F401
from src.screens.recipe_screen import RecipeScreen  # noqa: F401
from src.screens.settings_screen import SettingsScreen  # noqa: F401
from src.widgets.spinner_widget import SpinnerWidget  # noqa: F401


class WhatsForDinnerApp(App):
    """Root application class."""

    def build(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Register resource folders so Kivy finds them on Android too
        resource_add_path(os.path.join(base_dir, "kv"))
        resource_add_path(os.path.join(base_dir, "assets"))

        # Load KV by bare filename (resolved via resource paths)
        Builder.load_file("spinner.kv")

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(RecipeScreen(name="recipe"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm


if __name__ == "__main__":
    WhatsForDinnerApp().run()
