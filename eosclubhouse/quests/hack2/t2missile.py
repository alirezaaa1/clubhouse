from eosclubhouse.libquest import Quest
from eosclubhouse.system import App


class T2Missile(Quest):

    APP_NAME = 'com.endlessnetwork.missilemath'

    __quest_name__ = '''Terminal 2 - Missile Math'''
    __tags__ = ['pathway:games', 'difficulty:normal']
    __pathway_order__ = 131

    def setup(self):
        self._app = App(self.APP_NAME)

    def step_begin(self):
        if not self._app.is_installed():
            self.wait_confirm('NOTINSTALLED', confirm_label='App Center, got it.')
            return self.step_abort
        else:
            self.wait_confirm('GREET1')
            self.wait_confirm('GREET2', confirm_label="I'll remember that...")
            return self.step_launch

    def step_launch(self):
        self._app.launch()
        return self.step_complete_and_stop
