import appdaemon.plugins.hass.hassapi as hass

class Home(hass.Hass):
    def initialize(self):
        self.control = 'input_select.home_mode'
        self.light = self.args["light"]

        self.listen_state(self.on_home, self.control, new='Home')
    
    def on_home(self, entity, attribute, old, new, kwargs):
        if self.sun_down():
            self.turn_on(self.light, brightness=100)