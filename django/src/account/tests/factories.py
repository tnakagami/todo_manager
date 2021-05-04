import datetime
import pytz
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
# factory boy library
from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime

tzinfo = pytz.timezone(settings.TIME_ZONE)
UserModel = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    email = Sequence(lambda count: 'user{}@example.com'.format(count))
    screen_name = Sequence(lambda count: 'screen_name{}'.format(count))
    password = make_password('password')
    is_staff = False
    is_active = True
    date_joined = FuzzyDateTime(start_dt=timezone.datetime(2021, 1, 1, tzinfo=tzinfo))
