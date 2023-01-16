import appdaemon.plugins.hass.hassapi as hass

class ManageHomeMode(hass.Hass):

    def initialize(self):
        self.iphone = 'device_tracker.iphone_13_pro_max'
        self.mode_select = 'input_select.home_mode'

        self.on_away_timer = None
        self.on_vacation_timer = None
        self.disable_override_timer = None

        self.overridden_by_user = False
        self.mode_set_by_me = False

        if self.get_state(self.iphone) == "not_home":
            self.log("iPhone not at home. Setting timers")
            self.start_timers()
        else:
            self.log("iPhone is at home. Setting to home")
            self.try_set_mode('Home')
        
        self.listen_state(self.on_home, self.iphone, new='home')
        self.listen_state(self.on_not_home, self.iphone, new='not_home')
        self.listen_state(self.on_mode_change, self.mode_select)
    
    def try_set_mode(self, mode):
        if self.overridden_by_user:
            self.log(f"Currently overriden by user. Not setting {mode}")
            return
        
        current_mode = self.get_state(self.mode_select)
        if mode == current_mode:
            return

        self.mode_set_by_me = True
        self.select_option(self.mode_select, mode)
    
    def on_home(self, entity, attribute, old, new, kwargs):
        self.log("Detected back home")
        self.try_set_mode('Home')
        self.notify("Welcome back home!")

        self.try_cancel_timer(self.on_away_timer)
        self.try_cancel_timer(self.on_vacation_timer)

        self.on_away_timer = None
        self.on_vacation_timer = None
    
    def on_not_home(self, entity, attribute, old, new, kwargs):
        self.log("Detected no longer at home")
        self.start_timers()
    
    def on_mode_change(self, entity, attribute, old, new, kwargs):
        try:
            if self.mode_set_by_me:
                # I changed the mode, so ignore the change event
                self.log("Mode change detected. Initiated by me, so skipping")
                return
            else:
                self.log("Overriden. Ignoring changes for 1 hour")

            self.overridden_by_user = True

            self.try_cancel_timer(self.disable_override_timer)
            self.disable_override_timer = self.run_in(self.disable_override, 60 * 60)

        finally:
            self.mode_set_by_me = False
    
    def start_timers(self):
        self.on_away_timer = self.run_in(self.set_to_away, 60 * 30)
        self.on_vacation_timer = self.run_in(self.set_to_vacation, 60 * 60 * 24)
    
    def set_to_away(self, kwargs):
        self.try_set_mode('Away')

    def set_to_vacation(self, kwargs):
        self.try_set_mode('Vacation')
        self.notify("Looks like you're spending some time away! Enjoy!")
    
    def disable_override(self, kwargs):
        self.overridden_by_user = False
    
    def try_cancel_timer(self, timer):
        if timer == None:
            return
        
        self.cancel_timer(timer)