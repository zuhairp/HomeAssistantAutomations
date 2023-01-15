import appdaemon.plugins.hass.hassapi as hass

class MirrorSwitch(hass.Hass):

    def initialize(self):
        self.primary = self.args["primary"]

        self.listen_state(self.state_changed, self.primary, attribute="state")
        self.listen_state(self.brightness_changed, self.primary, attribute="brightness")

    def brightness_changed(self, entity, attribute, old, new, kwargs):
        self.log("Brightness changed")
        if old == None or new == None:
            # We'll take care of this with power toggles
            return
        
        if old == new:
            return

        for light in self.args["mirrors"]:
            self.turn_on(light, brightness=new)
    
    def state_changed(self, entity, attribute, old, new, kwargs):
        self.log("Power state changed")
        if old == new:
            return
        
        for light in self.args["mirrors"]:
            self.log(f"Light = {light}")
            if new == "on":
                self.turn_on(light)
            else:
                self.turn_off(light)
