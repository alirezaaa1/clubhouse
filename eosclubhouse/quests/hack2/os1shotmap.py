from eosclubhouse.libquest import Quest
from eosclubhouse.system import App


class OSOneshotMap(Quest):

    APP_NAME = 'org.gnome.Terminal'

    __tags__ = ['pathway:operating system', 'difficulty:hard', 'skillset:LaunchQuests']
    __pathway_order__ = 255

    TOTAL_MESSAGES = 34

    def setup(self):
        self._app = App(self.APP_NAME)
        return self.step_begin

    def step_begin(self):
        self.deploy_file('treasuremeowp', '~/yarnbasket/', override=True)
        self.wait_confirm('1')
        self.wait_confirm('2')
        self.ask_for_app_launch(self._app, pause_after_launch=2, message_id='LAUNCH')

        return self.step_main_loop, 3

    def step_main_loop(self, message_index):
        if message_index > self.TOTAL_MESSAGES:
            self.wait_confirm('END')
            return self.step_complete_and_stop
        elif message_index < 1:
            message_index = 1

        message_id = str(message_index)

        def _direction_choice(direction_choice_var):
            return direction_choice_var

        action = self.show_choices_message(message_id, ('BAK', _direction_choice, True),
                                           ('FWD', _direction_choice, False)).wait()
        go_back = action.future.result()

        if go_back:
            message_index -= 1
        else:
            message_index += 1

        return self.step_main_loop, message_index
