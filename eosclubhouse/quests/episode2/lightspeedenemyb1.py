from eosclubhouse.apps import LightSpeed
from eosclubhouse.libquest import Quest
from eosclubhouse.system import Sound

# @todo: This quest only changes a few lines from the LightSpeedEnemyA2 quest, so we should make
# sure that we use a common base but only after both quests' development is finished (otherwise,
# optimizing ATM may end up making things more complicated).


class LightSpeedEnemyB1(Quest):

    APP_NAME = 'com.endlessm.LightSpeed'
    SCREEN_HEIGHT = 1004

    __available_after_completing_quests__ = ['LightSpeedEnemyA3']

    def __init__(self):
        super().__init__('LightSpeedEnemyB1', 'saniel')
        self._app = LightSpeed()

    def step_begin(self):
        self.ask_for_app_launch(self._app)

        self.show_hints_message('EXPLANATION')
        self._app.set_level(6)

        self.pause(1)
        if self._has_enemies():
            msg_id = 'CODE2'
        else:
            msg_id = 'CODE1'

        return self.step_wait_for_flip, msg_id

    def _has_enemies(self):
        return self._app.get_js_property('enemyType2SpawnedCount') != 0

    @Quest.with_app_launched(APP_NAME)
    def step_wait_for_flip(self, code_msg_id):
        if not self._app.get_js_property('flipped') or self.debug_skip():
            self.wait_for_app_js_props_changed(self._app, ['flipped'])
        return self.step_code, code_msg_id

    @Quest.with_app_launched(APP_NAME)
    def step_code(self, code_msg_id):
        msg_to_show = code_msg_id
        if not self._app.get_js_property('flipped') or self.debug_skip():
            if self._app.get_js_property('playing'):
                return self.step_play

            # If we're not flipped nor playing, then we're in a Restart or Continue screens, and
            # thus ask the user to play.
            msg_to_show = 'ABOUTTOPLAY'

        if code_msg_id == 'CODE1':
            self._app.reveal_topic('spawn')
        elif code_msg_id == 'CODE2':
            self._app.reveal_topic('updateSquid')

        self.show_hints_message(msg_to_show)

        self.wait_for_app_js_props_changed(self._app, ['flipped', 'playing'])
        return self.step_code, code_msg_id

    @Quest.with_app_launched(APP_NAME)
    def step_play(self):
        self.show_hints_message('PLAYTEST')
        self.pause(10)

        min_property = 'enemyType2MinY'
        max_property = 'enemyType2MaxY'
        code_msg_id = 'CODE1'

        while not self.is_cancelled():
            min_y = self._app.get_js_property(min_property)
            max_y = self._app.get_js_property(max_property)

            if self.debug_skip():
                return self.step_success

            if not self._has_enemies():
                self.show_hints_message('NOENEMY')
                break

            if min_y is not None and max_y is not None:
                if min_y == max_y:
                    self.show_hints_message('NOTMOVING')
                    code_msg_id = 'CODE2'
                    break
                if min_y < -500 or max_y > self.SCREEN_HEIGHT + 500:
                    self.show_hints_message('OFFSCREEN')
                    code_msg_id = 'CODE2'
                    break

                return self.step_success

            self.wait_for_app_js_props_changed(self._app, [min_property, max_property])

        return self.step_wait_for_flip, code_msg_id

    def step_success(self):
        self.complete = True
        self.available = False

        Sound.play('quests/quest-complete')
        self.show_confirm_message('SUCCESS', confirm_label='Bye').wait()

        self.stop()
