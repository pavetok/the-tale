# coding: utf-8

from the_tale.common.utils import testcase

from the_tale.accounts.payments.goods import ResetHeroPreference
from the_tale.accounts.payments.price_list import PRICE_LIST

from the_tale.game.heroes.preferences import PREFERENCE_TYPE


class PriceListTests(testcase.TestCase):

    def setUp(self):
        super(PriceListTests, self).setUp()


    def test_all_preferences_in_prices(self):
        self.assertEqual(set(price.preference_type for price in PRICE_LIST if isinstance(price, ResetHeroPreference)),
                         set(PREFERENCE_TYPE.records))
