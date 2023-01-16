import appdaemon.plugins.hass.hassapi as hass

class Night(hass.Hass):
    def initialize(self):
        self.control = self.args["control"]

        self.off = self.args["turn_off"]
        self.dimmed = self.args["dimmed"]
        self.reset_brightness_at_sunrise = self.args["reset_brightness_at_sunrise"]
        self.on_at_sunrise = self.args["on_at_sunrise"]

        self.listen_state(self.on_activate, self.control, new="on")

        self.run_at_sunrise(self.restore_brightness)
        self.run_at_sunrise(self.turn_on_at_sunrise)
    
    def on_activate(self, entity, attribute, old, new, kwargs):
        self.save_brightnesses()
        for entity in self.dimmed:
            self.turn_on(entity, brightness=25)

        for entity in self.off:
            self.turn_off(entity)
        
        # Toggle back the control so it acts like a momentary button
        self.turn_off(self.control)
    
    def save_brightnesses(self):
        self.brightness = {}
        for entity in self.dimmed:
            self.turn_on(entity)
            self.brightness[entity] = self.get_state(entity, attribute="brightness")
    
    def restore_brightness(self, kwargs):
        for e, b in self.brightness.items():
            self.turn_on(e, brightness=b)
            self.turn_off()

    def turn_on_at_sunrise(self, kwargs):
        for entity in self.on_at_sunrise:
            self.turn_on(entity)
