from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.properties import ObjectProperty

from kivy.config import Config

# Set Default Window Size
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.write()

class MainUI(Screen):
    pass


class AddClueScreen(Screen):
    pass


class AddHintScreen(Screen):
    pass


class Manager(ScreenManager):
    """ Screen Manager for Kivy UI """
    main_ui  = ObjectProperty(None)
    add_clue = ObjectProperty(None)
    add_hint = ObjectProperty(None)


class KVRegioneer(App):
    """ This is a test application gui for Regioneer. """

    def __init__(self):
        # Make sure things are properly initialized
        super(KVRegioneer, self).__init__()

        # Main Elements of application

        # This is where the user will add/remove Locations
        self.LocationSelector = None

        # This is where the user will select the type of hint to add
        self.AddHintPopUp = None

        # This is where the user will add multiple 'hints' into Regioneer to denote proof of location
        self.AddProofPopUp = None

        # This is the listing of scripts to be executed upon location identification
        self.CustomScriptsPopUp = None

        self.manager = None

        ################################################################################################################
        # This is the listing of desktop settings that the user wants changed when a given location is identified      #
        # This will need to understand:                                                                                #
        #   QT:                                                                                                        #
        #       - kde                                                                                                  #
        #   GTK:                                                                                                       #
        #       - gnome (3+ only)                                                                                      #
        #       - cinnamon                                                                                             #
        #       - mate                                                                                                 #
        #       - xfce                                                                                                 #
        ################################################################################################################
        self.DesktopSettingsPopUp = None

    def build(self):
        """ Build the UI for the application. """

        # Register the individual UI pieces
        #Factory.register('LocationSelector', module='ui.LocationSelector')
        #Factory.register('AddHintPopUp', module='ui.AddHintPopUp')
        #Factory.register('AddProofPopUp', module='ui.AddProofPopUp')
        #Factory.register('CustomScriptsPopUp', module='ui.CustomScriptsPopUp')
        #Factory.register('DesktopSettingsPopUp', module='ui.DesktopSettingsPopUp')
        #Factory.register('WifiRowLayout', module='ui.WifiRowLayout')

        #self.LocationSelector = Factory.LocationSelector()
        #self.AddHintPopUp = Factory.AddHintPopUp()
        #self.AddProofPopUp = Factory.AddProofPopUp()
        #self.CustomScriptsPopUp = Factory.CustomScriptsPopUp()
        #self.DesktopSettingsPopUp = Factory.DesktopSettingsPopUp()

        #return Factory.AddHintPopUp()

        # Establish the Screen Manager
        self.manager = Manager(transition=WipeTransition())

        return self.manager


# Left side of main application
Builder.load_file('ui/location_view.kv')


# Hint Specifics
Builder.load_file('ui/tabbed_view.kv')
Builder.load_file('ui/hint_toolbar.kv')
Builder.load_file('ui/actions_view.kv')
Builder.load_file('ui/hint_view.kv')

# Load the main view
Builder.load_file('ui/main_ui.kv')

# Load additional screens
Builder.load_file('screens.kv')

if __name__ == "__main__":
    KVRegioneer().run()

