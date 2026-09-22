"""
What's for Dinner - Application entry point.

Bootstraps Kivy, registers resource paths, loads KV files,
and builds the ScreenManager.
"""

import os

from kivy.app import App
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager

from src.screens.home_screen import HomeScreen
from src.screens.recipe_screen import RecipeScreen
from src.screens.settings_screen import SettingsScreen


class WhatsForDinnerApp(App):
    """Root application class."""

    def build(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Register resource folders so Kivy finds them on Android too
        resource_add_path(os.path.join(base_dir, "kv"))
        resource_add_path(os.path.join(base_dir, "assets"))

        # Load KV files by bare filename (resolved via resource paths)
        Builder.load_file("spinner.kv")

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(RecipeScreen(name="recipe"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm


if __name__ == "__main__":
    WhatsForDinnerApp().run()
