import appdaemon.plugins.hass.hassapi as hass

class Away(hass.Hass):
    def initialize(self):
        self.control = 'input_select.home_mode'
        self.off = self.args["turn_off"]

        self.listen_state(self.on_away, self.control, new='Away')
    
    def on_away(self, entity, attribute, old, new, kwargs):
        for entity in self.off:
            self.turn_off(entity)