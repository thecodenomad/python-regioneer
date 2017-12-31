# Regioneer core imports
from utils.threadpool import ThreadPool


from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

from kivy.config import Config

from utils.startup import load_configuration_file

from core.models import ProfileManager

from utils.logger import get_logger

# Set Default Window Size
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.write()

NUM_THREADS = 4

_log = get_logger()

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


class LocationToolbar(BoxLayout):
    """
    This class is meant to handle the backend data modules using the ProfileManager class.
    """

    def __init__(self, **kwargs):
        super(LocationToolbar, self).__init__(**kwargs)
        self.pm = ProfileManager()
        _log.info("Created profile manager...")

    def add_profile(self, name=None):
        """ Add a new location. """
        _log.info("Yay adding a profile")
        #self.pm.add_empty_profile(name)

    def update(self, values):
        """ TODO: Needs to do something. """

    def remove(self):
        """ TODO: Needs to do something. """


class KVRegioneer(App):
    """ This is a test application gui for Regioneer. """

    def __init__(self):
        # Make sure things are properly initialized
        super(KVRegioneer, self).__init__()

        # Regioneer models
        self.profiles = load_configuration_file()

        # Main Elements of application
        self.tp = ThreadPool(NUM_THREADS)

        # This is where the user will add/remove Locations
        self.LocationSelector = None

        self.manager = None

        # # Start with default profiles
        # self.loc_profiles = []
        # # TODO: add above profiles for autopropogation

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

        self.current_location = None

    def _reset_threadpool(self, num_threads=NUM_THREADS):
        """ Re-establish a fresh threadpool. """

        if not self.tp.shutdown:
            self.tp.wait_and_shutdown()

        self.tp = ThreadPool(num_threads)

    def build(self):
        """ Build the UI for the application. """

        # Establish the Screen Manager
        self.manager = Manager(transition=WipeTransition())
        _log.info("Screen manager established.")

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

