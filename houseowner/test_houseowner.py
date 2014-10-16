import datetime
from django.utils import timezone
from houseowner.models import HouseOwner
from django.test import TestCase

class HousownerMethodtest(TestCase):
    def test_was_published_recently_with_future_poll(self):
        housownerjoin = HouseOwner(Houseownerjoinedthesite=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(housownerjoin.was_published_recently(), False)