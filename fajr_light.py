import appdaemon.plugins.hass.hassapi as hass
from dateutil import parser
from datetime import datetime
import pytz

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
        dt = parser.parse(new)
        if dt > datetime.now(pytz.utc):
            self.run_at(self.at_fajr, dt)
        else:
            self.log("Fajr time already past. Will reschedule at midnight")

    def at_fajr(self, kwargs):
        self.log("Turned on light")
        self.turn_on(self.fajr_light, brightness=50)