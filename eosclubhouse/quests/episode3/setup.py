from eosclubhouse.libquest import Quest
from eosclubhouse.system import Sound


class SetUp(Quest):

    def step_begin(self):
        self.wait_confirm('EXPLAIN')
        self.wait_confirm('EXPLAIN2')
        self.wait_confirm('EXPLAIN3')
        self.wait_confirm('EXPLAIN4')
        return self.step_success

    def step_success(self):
        self.wait_confirm('END')
        self.complete = True
        self.available = False
        Sound.play('quests/quest-complete')
        self.stop()
