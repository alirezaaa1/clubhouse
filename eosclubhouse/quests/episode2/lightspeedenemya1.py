from eosclubhouse.apps import LightSpeed
from eosclubhouse.libquest import Quest
from eosclubhouse.system import Sound


class LightSpeedEnemyA1(Quest):

    APP_NAME = 'com.endlessm.LightSpeed'

    __available_after_completing_quests__ = ['LightSpeedFix2', 'StealthDevice']

    def setup(self):
        self._app = LightSpeed()

    def step_begin(self):
        self.ask_for_app_launch(self._app)
        return self.step_newlevel

    @Quest.with_app_launched(APP_NAME)
    def step_newlevel(self):
        if self._app.get_js_property('flipped') or self.debug_skip():
            return self.step_changeenemy

        self.show_hints_message('NEWLEVEL')
        self._app.set_level(5)

        self.wait_for_app_js_props_changed(self._app, ['flipped'])
        return self.step_newlevel

    @Quest.with_app_launched(APP_NAME)
    def step_changeenemy(self):
        if not self._app.get_js_property('flipped') or self.debug_skip():
            self.show_hints_message('PLAYTEST')
            return self.step_play

        self._app.reveal_topic('spawn')

        self.show_hints_message('CHANGEENEMY')

        self.wait_for_app_js_props_changed(self._app, ['flipped'])
        return self.step_changeenemy

    @Quest.with_app_launched(APP_NAME)
    def step_play(self):
        enemy_count = self._app.get_js_property('enemyType1SpawnedCount')
        if (enemy_count is not None and enemy_count >= 2) or self.debug_skip():
            # @todo: Check if they spawned asteroids and go back
            # @todo: Timeout if nothing spawned in 5 seconds
            return self.step_success

        self.wait_for_app_js_props_changed(self._app, ['enemyType1SpawnedCount'])
        return self.step_play

    def step_success(self):
        self.complete = True
        self.available = False

        Sound.play('quests/quest-complete')
        self.show_confirm_message('SUCCESS', confirm_label='Bye').wait()

        self.stop()
