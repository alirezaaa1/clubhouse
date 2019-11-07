from eosclubhouse.libquest import Quest
from eosclubhouse.system import App


class OSOneshotMap(Quest):

    APP_NAME = 'org.gnome.Terminal'

    __tags__ = ['pathway:operating system', 'difficulty:hard', 'skillset:LaunchQuests']
    __pathway_order__ = 255

    def setup(self):
        self._app = App(self.APP_NAME)
        self._info_messages = self.get_loop_messages('OSONESHOTMAP', start=3)

    def step_begin(self):
        self.deploy_file('treasuremeowp', '~/yarnbasket/', override=True)
        self.deploy_file('rhyme', '~/yarnbasket/', override=True)
        self.wait_confirm('1')
        self.wait_confirm('2')
        self.ask_for_app_launch(self._app, pause_after_launch=2, message_id='LAUNCH')

        return self.step_main_loop

    def step_main_loop(self, message_index=0):
        message_id = self._info_messages[message_index]

        if message_id == self._info_messages[-1]:
            self.wait_confirm(message_id)
            return self.step_complete_and_stop

        options = []
        if message_id != self._info_messages[0]:
            options.append(('NOQUEST_NAV_BAK', None, -1))

        options.append(('NOQUEST_NAV_FWD', None, 1))

        action = self.show_choices_message(message_id, *options).wait()
        return self.step_main_loop, message_index + action.future.result()
