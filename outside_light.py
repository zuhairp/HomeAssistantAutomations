import appdaemon.plugins.hass.hassapi as hass

class OutsideLight(hass.Hass):
    def initialize(self):
        self.light = "light.outside_light_switch"

        self.run_at_sunrise(self.at_sunrise)
        self.run_at_sunset(self.at_sunset)

        if self.sun_down():
            self.log("Sun is currently down")
            self.turn_on(self.light)
        else:
            self.log("Sun is currently up")
            self.turn_off(self.light)
        
    def at_sunset(self, kwargs):
        self.turn_on(self.light)
        self.log("Turned on outside light")

    def at_sunrise(self, kwargs):
        self.turn_off(self.light)
        self.log("Turned off outside light")
    