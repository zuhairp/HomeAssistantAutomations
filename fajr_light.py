import appdaemon.plugins.hass.hassapi as hass

class FajrLight(hass.Hass):
    def initialize(self):
        self.fajr_light = "lights.bedroom_light_switch"

        # For future updates
        self.listen_state(self.schedule_fajr, "sensor.fajr_prayer")

        # For today's
        fajr = self.get_state("sensor.fajr_prayer")
        self.schedule_fajr(entity='', attribute='', old='', new=fajr, kwargs={})

    def schedule_fajr(self, entity, attribute, old, new, kwargs):
        self.log(f"Scheduling light for {new}")
        self.run_at(self.at_fajr, new)

    def at_fajr(self, kwargs):
        self.log("Turned on light")
        self.turn_on(self.fajr_light, brightness=50)