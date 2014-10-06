# coding: utf-8
import random

from textgen.words import Noun

from dext.utils import s11n

from django.core.management.base import BaseCommand
from django.db import transaction

from the_tale.common.utils.logic import run_django_command

from the_tale.game.balance import constants as c
from the_tale.game import names
from the_tale.game.relations import GENDER, RACE
from the_tale.game.prototypes import TimePrototype

from the_tale.game.map.roads.models import Road
from the_tale.game.map.places.models import Place
from the_tale.game.map.places.prototypes import PlacePrototype
from the_tale.game.map.places.conf import places_settings
from the_tale.game.map.places.storage import places_storage
from the_tale.game.map.roads.storage import roads_storage

from the_tale.game.persons.prototypes import PersonPrototype
from the_tale.game.persons.storage import persons_storage
from the_tale.game.persons.conf import persons_settings
from the_tale.game.persons.relations import PERSON_TYPE


DESCRIPTION = u'''
«…Город наш появился совсем недавно. Исследования далёких земель увенчались успехом, и было найдено подходящее место. Учёные, специалисты и некоторые герои признали, что город, здесь основанный, имеет все шансы стать крупным и богатым. И началось...

А как бы оно не началось, если это новый город, а значит, новые возможности? Народ сразу потянулся в перспективное поселение. Многие, как всегда, погибли по пути, в когтях монстров, некоторые, в связи с этим, передумали и повернули назад, но часть всё же добралась до места. Как только возвели какой-никакой частокол, подняли вопрос о “наболевшем”... о власти. Кандидатов было много поначалу, но Каммадин, алхимик с внушительным стажем и тёмной репутацией, быстро сократил их количество до четырёх: он сам, бюрократ из человеческого племени, якобы большой специалист в градоуправлении, дварф с курчавой бородой, тамбурином и неизменным перегаром, а также эльфка-магичка Саннаэль, быстро прослывшая в городе не иначе, как “наша грымза”…»
'''


class Command(BaseCommand):

    help = 'create places'

    def handle(self, *args, **kwargs):
        try:
            self.run()
        except Exception:
            import sys
            import traceback
            traceback.print_exc()
            print sys.exc_info()

            raise


    def _create_place(self, x, y, roads_to, name_forms=None):

        if name_forms is None:
            name_forms=Noun.fast_construct(u'%dx%d' % (x, y))

        return self.create_place(name_forms=name_forms,
                                 x=x,
                                 y=y,
                                 size=1,
                                 is_frontier=True,
                                 roads_to=roads_to)

    def run(self, *args, **kwargs):

        # to sync map size and do other unpredictable operations
        run_django_command(['map_update_map'])

        self.INITIAL_PERSON_POWER = persons_storage.get_medium_power_for_person() * 5

        name_1 = Noun(normalized=u'Каммадин',
                     forms=(u'Каммадин', u'Каммадина', u'Каммадину', u'Каммадина', u'Каммадином', u'Каммадине',
                            u'Каммадины', u'Каммадинов', u'Каммадинам', u'Каммадинов', u'Каммадинами', u'Каммадинах'),
                     properties=(u'мр'))

        name_2 = Noun(normalized=u'Путятя',
                     forms=(u'Путятя', u'Путяти', u'Путяте', u'Путятю', u'Путятей', u'Путяте',
                            u'Путяти', u'Путять', u'Путятям', u'Путять', u'Путятями', u'Путятях'),
                     properties=(u'мр'))

        name_3 = Noun(normalized=u'Вилфредд',
                     forms=(u'Вилфредд', u'Вилфредда', u'Вилфредду', u'Вилфредда', u'Вилфреддом', u'Вилфредде',
                            u'Вилфреддов', u'Вилфреддов', u'Вилфреддам', u'Вилфреддов', u'Вилфреддами', u'Вилфреддах'),
                     properties=(u'мр'))

        name_4 = Noun(normalized=u'Саннаэль',
                     forms=(u'Саннаэль', u'Саннаэль', u'Саннаэль', u'Саннаэль', u'Саннаэль', u'Саннаэль',
                            u'Саннаэли', u'Саннаэлей', u'Саннаэлям', u'Саннаэлей', u'Саннаэлями', u'Саннаэлях'),
                     properties=(u'жр'))


        with transaction.atomic():

            persons = [(name_1, RACE.ELF, GENDER.MASCULINE, PERSON_TYPE.ALCHEMIST),
                       (name_2, RACE.HUMAN, GENDER.MASCULINE, PERSON_TYPE.BUREAUCRAT),
                       (name_3, RACE.DWARF, GENDER.MASCULINE, PERSON_TYPE.BARD),
                       (name_4, RACE.ELF, GENDER.FEMININE, PERSON_TYPE.MAGICIAN)]

            self.create_place(x=36, y=13,
                               roads_to=[places_storage[2]],
                               persons=persons,
                               description=DESCRIPTION,
                               is_frontier=True,
                               name_forms=Noun(normalized=u'Таргард',
                                               forms=(u'Таргард', u'Таргарда', u'Таргарду', u'Таргард', u'Таргардом', u'Таргарде',
                                                      u'Таргарды', u'Таргардов', u'Таргардам', u'Таргарды', u'Таргардами', u'Таргардах'),
                                               properties=(u'мр')))

        # update map with new places
        run_django_command(['map_update_map'])


    @transaction.atomic
    def create_place(self, x, y, roads_to, persons=(), name_forms=None, is_frontier=False, description=u''): # pylint: disable=R0914

        # place_power = int(max(place.power for place in places_storage.all()) * float(size) / places_settings.MAX_SIZE)


        # place_power_steps = int(places_settings.POWER_HISTORY_LENGTH / c.MAP_SYNC_TIME)
        # place_power_per_step = (place_power / place_power_steps) + 1

        place = PlacePrototype.create( x=x,
                                       y=y,
                                       name_forms=name_forms,
                                       is_frontier=is_frontier,
                                       size=1)
        place.description = description
        place.save()

        # initial_turn = TimePrototype.get_current_turn_number() - places_settings.POWER_HISTORY_LENGTH
        # for i in xrange(place_power_steps):
        #     place.push_power(int(initial_turn+i*c.MAP_SYNC_TIME), int(place_power_per_step))

        for person_name_forms, race, gender, tp in persons:
            person = PersonPrototype.create(place=place,
                                            race=race,
                                            gender=gender,
                                            tp=tp,
                                            name_forms=person_name_forms)

        place.sync_persons(force_add=True)

        power_delta = self.INITIAL_PERSON_POWER

        for person in place.persons:
            person.fill_power_evenly(power_delta)
            person.save()
            # power_delta /= 2

        place.sync_race()
        place.save()

        for destination in roads_to:
            Road.objects.create(point_1=place._model, point_2=destination._model)

        persons_storage.update_version()
        places_storage.update_version()
        roads_storage.update_version()

        return place
