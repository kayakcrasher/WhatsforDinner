"""
What's for Dinner - Main application entry point.

This module bootstraps the Kivy application, loads KV definitions,
and wires the screen manager.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, BooleanProperty


class HomeScreen(Screen):
    """
    Main screen: user taps spin, animation plays, recipe appears.
    """
    current_recipe = StringProperty("")
    is_spinning = BooleanProperty(False)


class RecipeScreen(Screen):
    """
    Displays full recipe details (ingredients, steps).
    """
    pass


class SettingsScreen(Screen):
    """
    Settings + upgrade to paid tier.
    """
    pass


class WhatsForDinnerApp(App):
    """
    Root application class. Builds the ScreenManager.
    """

    def build(self):
        # Load KV files from assets/animations/
        Builder.load_file("assets/animations/spinner.kv")

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(RecipeScreen(name="recipe"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm


if __name__ == "__main__":
    WhatsForDinnerApp().run()
