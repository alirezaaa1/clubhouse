from eosclubhouse.apps import Fizzics
from eosclubhouse.libquest import Quest
from eosclubhouse.system import Sound


class FizzicsCode1(Quest):

    def __init__(self):
        super().__init__('Fizzics Code 1', 'ada')
        self._app = Fizzics()

    def step_begin(self):
        self.ask_for_app_launch(self._app, pause_after_launch=2)
        return self.step_flip

    @Quest.with_app_launched(Fizzics.APP_NAME)
    def step_flip(self):
        if self._app.get_js_property('flipped'):
            return self.step_unlock

        Sound.play('quests/step-forward')
        self.show_hints_message('FLIP')
        while not self._app.get_js_property('flipped') and not self.is_cancelled():
            self.wait_for_app_js_props_changed(self._app, ['flipped'])

        return self.step_unlock

    def _is_panel_unlocked(self):
        lock_state = self.gss.get('lock.fizzics.2')
        return lock_state is not None and lock_state.get('locked', True)

    @Quest.with_app_launched(Fizzics.APP_NAME)
    def step_unlock(self):
        if self._is_panel_unlocked():
            return self.step_explanation1

        Sound.play('quests/step-forward')
        self.show_hints_message('UNLOCK')
        while not self._is_panel_unlocked() and not self.is_cancelled():
            self.connect_gss_changes().wait()

        return self.step_explanation1

    def _has_radius_changed(self, prev_radius):
        return self._app.get_js_property('radius_0', prev_radius) != prev_radius

    @Quest.with_app_launched(Fizzics.APP_NAME)
    def step_explanation1(self):
        Sound.play('quests/step-forward')
        self.show_hints_message('EXPLANATION1')

        prev_radius = self._app.get_js_property('radius_0', 0)
        while not self._has_radius_changed(prev_radius) and not self.is_cancelled():
            # @todo: Connect to app property changes instead of
            # polling. This needs a fix in Clippy. See
            # https://phabricator.endlessm.com/T25359
            self.pause(0.5)

        return self.step_explanation2

    @Quest.with_app_launched(Fizzics.APP_NAME)
    def step_explanation2(self):
        Sound.play('quests/step-forward')
        self.show_hints_message('EXPLANATION2')

        # Add a delay, otherwise this would get triggered by clicking on the + multiple times
        self.pause(4)

        # @todo: this quest doesn't check if the radious was chenged
        # with code, as the EXPLANATION2 asks the user to do.
        prev_radius = self._app.get_js_property('radius_0', 0)
        while not self._has_radius_changed(prev_radius) and not self.is_cancelled():
            # @todo: Connect to app property changes instead of
            # polling. This needs a fix in Clippy. See
            # https://phabricator.endlessm.com/T25359
            self.pause(0.5)

        return self.step_end

    def step_end(self):
        Sound.play('quests/step-forward')
        self.complete = True
        self.available = False
        Sound.play('quests/quest-complete')
        self.show_message('END', choices=[('Bye', self.stop)])
