from eosclubhouse.libquest import Quest
from eosclubhouse.system import Desktop


class Migration(Quest):

    __tags__ = ['pathway:games', 'skillset:Veteran']

    def setup(self):
        self.skippable = True

    def step_begin(self):
        for msgid in ['WELCOME', 'WELCOME2']:
            self.wait_confirm(msgid)
        return self.step_open_clubhouse

    def step_open_clubhouse(self):
        self.show_hints_message('OPENIT')
        Desktop.set_hack_icon_pulse(True)
        while not Desktop.is_app_in_foreground('com.hack_computer.Clubhouse'):
            self.pause(5)
        # wait for the user to open the clubhouse
        return self.step_explain_old_apps

    def step_explain_old_apps(self):
        Desktop.set_hack_icon_pulse(False)
        # explain what we did to the old apps
        for msgid in ['OLDSTUFF1', 'OLDSTUFF2', 'OLDSTUFF3',
                      'OLDSTUFF4', 'OLDSTUFF5']:
            self.wait_confirm(msgid)
        return self.step_explain_new_stuff

    def step_explain_new_stuff(self):
        # explain hack mode
        for msgid in ['NEWSTUFF', 'HACKMODE1', 'HACKMODE2',
                      'HACKMODE3', 'HACKMODE4', 'HACKMODE5']:
            self.wait_confirm(msgid)
        return self.step_explain_activities

    def step_explain_activities(self):
        # explain activities and how to play them
        for msgid in ['ACTIVITIES1', 'ACTIVITIES2', 'ACTIVITIES3']:
            self.wait_confirm(msgid)
        return self.step_explain_profile

    def step_explain_profile(self):
        # explain how the profile works and how to change your name
        for msgid in ['PROFILE1', 'PROFILE2', 'PROFILE3']:
            self.wait_confirm(msgid)
        action = self.show_choices_message('PROFILE_ASK', ('PROFILE_POS', None, True),
                                           ('PROFILE_NEG', None, False)).wait()
        if action.future.result():
            for msgid in ['PROFILE_CHANGENAME1', 'PROFILE_CHANGENAME2',
                          'PROFILE_CHANGENAME3', 'PROFILE_CHANGENAME4']:
                self.wait_confirm(msgid)
        return self.step_last

    def step_last(self):
        self.wait_confirm('END1')
        self.wait_confirm('END2')
        return self.step_complete_and_stop
