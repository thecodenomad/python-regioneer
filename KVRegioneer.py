from kivy.app import App
from kivy.factory import Factory


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
        Factory.register('LocationSelector', module='ui.LocationSelector')
        Factory.register('AddHintPopUp', module='ui.AddHintPopUp')
        Factory.register('AddProofPopUp', module='ui.AddProofPopUp')
        Factory.register('CustomScriptsPopUp', module='ui.CustomScriptsPopUp')
        Factory.register('DesktopSettingsPopUp', module='ui.DesktopSettingsPopUp')
        Factory.register('WifiRowLayout', module='ui.WifiRowLayout')

        self.LocationSelector = Factory.LocationSelector()
        self.AddHintPopUp = Factory.AddHintPopUp()
        self.AddProofPopUp = Factory.AddProofPopUp()
        self.CustomScriptsPopUp = Factory.CustomScriptsPopUp()
        self.DesktopSettingsPopUp = Factory.DesktopSettingsPopUp()

        return Factory.LocationSelector()


if __name__ == "__main__":
    KVRegioneer().run()

