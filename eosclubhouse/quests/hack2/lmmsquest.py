from eosclubhouse.libquest import Quest
from eosclubhouse.system import App


class LMMSQuest(Quest):

    APP_NAME = 'io.lmms.LMMS'

    __tags__ = ['pathway:art', 'difficulty:medium', 'skillset:LaunchQuests']
    __pathway_order__ = 300

    def setup(self):
        self._app = App(self.APP_NAME)
        self._info_messages = self.get_loop_messages('INFO')

    def step_begin(self):
        if not self._app.is_installed():
            self.wait_confirm('NOTINSTALLED', confirm_label='Got it!')
            return self.step_abort

        self.wait_confirm('LAUNCH')
        self._app.launch()
        self.pause(4)
        return self.step_info_loop

    def step_info_loop(self, message_index=0):
        message_id = self._info_messages[message_index]

        options = [
            ('NOQUEST_NAV_BAK', None, -1),
            ('NOQUEST_NAV_FWD', None, 1),
        ]

        if message_id == self._info_messages[-1]:
            options.append(('QUIT', None, 0))

        action = self.show_choices_message(message_id, *options).wait()

        chosen_action = action.future.result()

        if chosen_action == 0:
            self.wait_confirm('BYE')
            return self.step_complete_and_stop
        else:
            return self.step_info_loop, message_index + chosen_action
