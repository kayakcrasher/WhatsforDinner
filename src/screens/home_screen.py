from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    current_recipe = StringProperty("")
    is_spinning = BooleanProperty(False)

    def spin(self):
        # Implemented in the next step
        pass
