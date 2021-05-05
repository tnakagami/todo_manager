import datetime
import pytz
from django.conf import settings
from django.utils import timezone
from factory import LazyAttribute, Sequence, post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime, FuzzyInteger
from todolist import models
tzinfo = pytz.timezone(settings.TIME_ZONE)

class TaskFactory(DjangoModelFactory):
    class Meta:
        model = models.Task

    title = Sequence(lambda count: 'title{}'.format(count))
    text = Sequence(lambda count: '# post text\ntext {}'.format(count))
    is_done = False
    point = FuzzyInteger(1, 1000)
    target_date = FuzzyDateTime(start_dt=timezone.datetime(2021, 1, 1, tzinfo=tzinfo))
    created_at = FuzzyDateTime(start_dt=timezone.datetime(2021, 1, 1, tzinfo=tzinfo))
    updated_at = FuzzyDateTime(start_dt=timezone.datetime(2021, 1, 1, tzinfo=tzinfo))
