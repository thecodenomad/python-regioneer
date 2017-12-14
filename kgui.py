from kivy.app import App
from kivy.clock import Clock
from kivy.properties import BooleanProperty

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.recycleview import RecycleView

# Disabled imports
# from kivy.uix.button import Label


class WifiRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(WifiRecycleView, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(10)]


class HintAddButton(Button):
    """ The Add Hint Button, this is required to enable/disable it"""
    enabled = BooleanProperty(True)


class AddHintPopup(Popup):
    """ Hint Wizard """


class RLayout(GridLayout):
    """ Main Regioneer application Layout """

    def add_hint_popup(self):
        p = AddHintPopup()
        p.open()


class RegioneerApp(App):
    def build(self):
        return RLayout()


if __name__ == "__main__":
    RegioneerApp().run()
