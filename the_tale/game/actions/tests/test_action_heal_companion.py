# coding: utf-8
import mock

from the_tale.common.utils import testcase

from the_tale.game.logic_storage import LogicStorage

from the_tale.game.companions import storage as companions_storage
from the_tale.game.companions import logic as companions_logic

from the_tale.game.logic import create_test_map
from the_tale.game.actions import prototypes
from the_tale.game.abilities.deck.help import Help
from the_tale.game.abilities.relations import HELP_CHOICES
from the_tale.game.prototypes import TimePrototype

from the_tale.game.abilities.tests.helpers import UseAbilityTaskMixin


class HealCompanionActionTest(UseAbilityTaskMixin, testcase.TestCase):
    PROCESSOR = Help

    def setUp(self):
        super(HealCompanionActionTest, self).setUp()

        create_test_map()

        self.account = self.accounts_factory.create_account()

        self.storage = LogicStorage()
        self.storage.load_account_data(self.account)

        self.hero = self.storage.accounts_to_heroes[self.account.id]

        self.companion_record = companions_storage.companions.enabled_companions().next()
        self.hero.set_companion(companions_logic.create_companion(self.companion_record))

        self.action_idl = self.hero.actions.current_action

        with self.check_increased(lambda: self.hero.companion.healed_at):
            self.action_heal_companion = prototypes.ActionHealCompanionPrototype.create(hero=self.hero)


    def test_create(self):
        self.assertEqual(self.action_idl.leader, False)
        self.assertEqual(self.action_heal_companion.leader, True)
        self.assertEqual(self.action_heal_companion.bundle_id, self.action_heal_companion.bundle_id)
        self.assertEqual(self.action_heal_companion.percents, 0)
        self.storage._test_save()


    def test_processed__no_companion(self):
        self.hero.remove_companion()
        self.storage.process_turn(continue_steps_if_needed=False)
        self.assertEqual(len(self.hero.actions.actions_list), 1)
        self.assertEqual(self.hero.actions.current_action, self.action_idl)
        self.storage._test_save()


    def test_processed__max_health(self):
        self.assertEqual(self.hero.companion.health, self.hero.companion.max_health)

        self.storage.process_turn(continue_steps_if_needed=False)
        self.assertEqual(len(self.hero.actions.actions_list), 1)
        self.assertEqual(self.hero.actions.current_action, self.action_idl)
        self.storage._test_save()


    def test_not_ready(self):
        self.hero.companion.health = 1

        self.storage.process_turn()

        self.assertEqual(len(self.hero.actions.actions_list), 2)
        self.assertEqual(self.hero.actions.current_action, self.action_heal_companion)
        self.assertTrue(self.hero.companion.health, 1)
        self.assertTrue(self.action_heal_companion.percents > 0)
        self.storage._test_save()

    def test_ability_heal_companion(self):

        self.hero.companion.health = 1

        with self.check_increased(lambda: self.action_heal_companion.percents):
            with self.check_increased(lambda: self.hero.companion.health):
                ability = self.PROCESSOR()

                with mock.patch('the_tale.game.actions.prototypes.ActionBase.get_help_choice', lambda x: HELP_CHOICES.HEAL_COMPANION):
                    self.assertTrue(ability.use(**self.use_attributes(hero=self.hero, storage=self.storage)))


    def test_ability_heal_companion__processed_when_healed(self):

        self.hero.companion.health -= 1

        with self.check_increased(lambda: self.action_heal_companion.percents):
            with self.check_increased(lambda: self.hero.companion.health):
                ability = self.PROCESSOR()

                with mock.patch('the_tale.game.actions.prototypes.ActionBase.get_help_choice', lambda x: HELP_CHOICES.HEAL_COMPANION):
                    self.assertTrue(ability.use(**self.use_attributes(hero=self.hero, storage=self.storage)))

        self.assertTrue(self.action_heal_companion.percents, 1)
        self.assertEqual(self.action_heal_companion.state, self.action_heal_companion.STATE.PROCESSED)


    def test_ability_heal_companion__full_action(self):

        self.hero.companion.health = 1

        with self.check_increased(lambda: self.action_heal_companion.percents):
            with self.check_increased(lambda: self.hero.companion.health):
                while self.action_heal_companion.state != self.action_heal_companion.STATE.PROCESSED:
                    ability = self.PROCESSOR()

                    with mock.patch('the_tale.game.actions.prototypes.ActionBase.get_help_choice', lambda x: HELP_CHOICES.HEAL_COMPANION):
                        self.assertTrue(ability.use(**self.use_attributes(hero=self.hero, storage=self.storage)))


    def test_full(self):
        self.hero.companion.health = 1

        current_time = TimePrototype.get_current_time()

        while len(self.hero.actions.actions_list) != 1:
            self.storage.process_turn(continue_steps_if_needed=False)
            current_time.increment_turn()

        self.assertTrue(self.action_idl.leader)
        self.assertEqual(self.hero.companion.health, 1)

        self.storage._test_save()