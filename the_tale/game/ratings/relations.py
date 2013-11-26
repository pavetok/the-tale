# coding: utf-8

from rels.django import DjangoEnum


class RATING_TYPE(DjangoEnum):
    records = ( ('MIGHT', 'might', u'Могущество'),
                 ('BILLS', 'bills', u'Принятые законы'),
                 ('POWER', 'power', u'Сила героя'),
                 ('LEVEL', 'level', u'Уровень героя'),
                 ('PHRASES', 'phrases', u'Добавленные фразы'),
                 ('PVP_BATTLES_1x1_NUMBER', 'pvp_battles_1x1_number', u'Сражения в PvP'),
                 ('PVP_BATTLES_1x1_VICTORIES', 'pvp_battles_1x1_victories', u'Победы в PvP'),
                 ('REFERRALS_NUMBER', 'referrals_number', u'Последователи'),
                 ('ACHIEVEMENTS_POINTS', 'achievements_points', u'Очки достижений'))
