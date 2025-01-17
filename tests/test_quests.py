#
# Copyright © 2020 Endless OS Foundation LLC.
#
# This file is part of clubhouse
# (see https://github.com/endlessm/clubhouse).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
import datetime

from eosclubhouse.libquest import Registry, NoMessageIdError
from eosclubhouse.utils import QuestStringCatalog
from eosclubhouse.system import GameStateService
from clubhouseunittest import ClubhouseTestCase, define_quest, \
    define_questset, setup_episode


class TestQuests(ClubhouseTestCase):

    def setUp(self):
        Registry.load_current_episode()

    def test_show_message_can_raise_custom_error(self):
        """Tests that Quests raise a custom error when a message ID is not in the catalog."""

        quest_class = define_quest('PhonyQuest')
        quest = quest_class()

        string_catalog = QuestStringCatalog._csv_dict
        QuestStringCatalog.set_key_value_from_csv_row(('PHONYQUEST_HELLO',
                                                       '', '', '', '', ''),
                                                      string_catalog)

        # The short and full forms should not raise:
        quest.show_message('HELLO')
        quest.show_message('PHONYQUEST_HELLO')

        with self.assertRaises(NoMessageIdError):
            quest.show_message('INEXISTENT_MESSAGE')

    def test_default_main_character(self):
        '''Tests there is some default main character when not provided in the catalog.'''
        QuestA = define_quest('QuestA')

        PhonyAlice = define_questset('PhonyAlice', 'web', 'alice')
        PhonyAlice.__quests__ = [QuestA]

        setup_episode([PhonyAlice()])

        quest_a = Registry.get_quest_by_name('QuestA')
        self.assertEqual(quest_a.get_main_character(), 'alice')
        self.assertNotEqual(quest_a.get_main_character(), '')

    def test_items_on_completion(self):
        '''Tests the __items_on_completion__ use.'''
        values_to_test = [({}, {'consume_after_use': False, 'used': False}),
                          ({'consume_after_use': True}, {'consume_after_use': True, 'used': False}),
                          ({'used': True}, {'consume_after_use': False, 'used': True}),
                          ({'consume_after_use': True, 'used': True}, {'consume_after_use': True,
                                                                       'used': True}),
                          ({'consume_after_use': False, 'used': False}, {'consume_after_use': False,
                                                                         'used': False})]

        for i in range(len(values_to_test)):
            value_to_set, value_to_expect = values_to_test[i]

            quest_class = define_quest('Quest{}'.format(i))
            key_name = 'item.key.{}'.format(i)
            quest_class.__items_on_completion__ = {key_name: value_to_set}

            quest = quest_class()
            # Saving without completing the quest.
            quest.save_conf()

            self.assertIsNone(GameStateService().get(key_name))

            # Saving after completing the quest.
            quest.complete = True
            quest.save_conf()

            value_in_gss = GameStateService().get(key_name)
            self.assertEqual(value_in_gss, value_to_expect)

    def test_is_named_quest_complete(self):
        '''Tests that quests can check if other quest is completed.'''
        quest_a_class = define_quest('QuestA')
        quest_b_class = define_quest('QuestB')

        quest_a = quest_a_class()
        quest_a.complete = True
        quest_a.save_conf()

        quest_b = quest_b_class()
        self.assertTrue(quest_b.is_named_quest_complete('QuestA'))

    def test_conf_on_completion(self):
        '''Tests the __conf_on_completion__ use.'''
        key_name = 'special.key.1'
        quest_class = define_quest('QuestA')
        quest_class.__conf_on_completion__ = {key_name: {'answer': 42}}

        quest = quest_class()
        # Saving without completing the quest.
        quest.save_conf()

        self.assertIsNone(GameStateService().get(key_name))

        # Saving after completing the quest.
        quest.complete = True
        quest.save_conf()

        value_in_gss = GameStateService().get(key_name)
        self.assertTrue(value_in_gss, {'answer': 42})

    def test_conf_save_and_load(self):
        '''Tests how to load and save custom configuration.'''
        quest_a_class = define_quest('QuestA')
        quest_b_class = define_quest('QuestB')
        quest_a1 = quest_a_class()
        self.assertEqual(quest_a1.get_conf('hints_given'), None)
        quest_a1.set_conf('hints_given', True)
        self.assertEqual(quest_a1.get_conf('hints_given'), True)
        quest_a1.save_conf()

        # This is a new instance of QuestA. Load happens automatically
        # on instantiation:
        quest_a2 = quest_a_class()
        self.assertEqual(quest_a2.get_conf('hints_given'), True)

        # We can also get the conf from another quest:
        quest_b = quest_b_class()
        conf = quest_b.get_named_quest_conf('QuestA', 'hints_given')
        self.assertEqual(conf, True)

    def test_available(self):
        '''Tests quest availability flags.'''
        QuestA = define_quest('QuestAvailable')

        PhonyAlice = define_questset('PhonyAlice', 'web', 'alice')
        PhonyAlice.__quests__ = [QuestA]

        setup_episode([PhonyAlice()])

        quest_a = Registry.get_quest_by_name('QuestAvailable')
        self.assertEqual(quest_a.available, True)

        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow1 = today + datetime.timedelta(days=2)

        # Testing available_since
        quest_a.available_until = ''
        quest_a.available_since = tomorrow.strftime('%Y-%m-%d')
        self.assertEqual(quest_a.available, False)
        quest_a.available_since = yesterday.strftime('%Y-%m-%d')
        self.assertEqual(quest_a.available, True)

        # Testing available_until
        quest_a.available_since = ''
        quest_a.available_until = yesterday.strftime('%Y-%m-%d')
        self.assertEqual(quest_a.available, False)
        quest_a.available_until = tomorrow.strftime('%Y-%m-%d')
        self.assertEqual(quest_a.available, True)

        # Testing available_since and available_until
        quest_a.available_since = yesterday.strftime('%Y-%m-%d')
        quest_a.available_until = yesterday.strftime('%Y-%m-%d')
        self.assertEqual(quest_a.available, False)

        quest_a.available_since = yesterday.strftime('%Y-%m-%d')
        quest_a.available_until = tomorrow.strftime('%Y-%m-%d')
        self.assertEqual(quest_a.available, True)

        quest_a.available_since = today.strftime('%Y-%m-%d')
        quest_a.available_until = tomorrow.strftime('%Y-%m-%d')
        self.assertEqual(quest_a.available, True)

        quest_a.available_since = today.strftime('%Y-%m-%d')
        quest_a.available_until = today.strftime('%Y-%m-%d')
        self.assertEqual(quest_a.available, True)

        quest_a.available_since = tomorrow.strftime('%Y-%m-%d')
        quest_a.available_until = tomorrow1.strftime('%Y-%m-%d')
        self.assertEqual(quest_a.available, False)
