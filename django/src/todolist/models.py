from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy
from django.core.validators import MinValueValidator

User = get_user_model()

class TaskCategory(models.Model):
    name = models.CharField(ugettext_lazy('category name'), max_length=64)

    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return self.name

class Task(models.Model):
    # user
    user = models.ForeignKey(User, verbose_name=ugettext_lazy('user'), on_delete=models.CASCADE)
    # タスクのタイトル
    title = models.CharField(ugettext_lazy('title'), max_length=64)
    # タスクの内容
    text = models.TextField(ugettext_lazy('detail'))
    # タスクの状態
    is_done = models.BooleanField(ugettext_lazy('doing or done'), default=False)
    # ポイント
    point = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    # 種別
    category = models.ForeignKey(TaskCategory, verbose_name=ugettext_lazy('category'), on_delete=models.PROTECT)
    # タスク実施日
    limit_date = models.DateTimeField(ugettext_lazy('limit date'), default=timezone.localdate)
    # タスク完了日
    complete_date = models.DateTimeField(ugettext_lazy('complete date'), default=timezone.now)
    # 作成日時
    created_at = models.DateTimeField(ugettext_lazy('create time'), default=timezone.now)
    # 更新日時
    updated_at = models.DateTimeField(ugettext_lazy('update time'), default=timezone.now)

    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return self.title

class PointHistory(models.Model):
    # user
    user = models.ForeignKey(User, verbose_name=ugettext_lazy('user'), on_delete=models.CASCADE)
    # 使用したポイント
    used_point = models.IntegerField(ugettext_lazy('used point'), validators=[MinValueValidator(0)], default=0)
    # 使用日
    used_date = models.DateTimeField(ugettext_lazy('used date'), default=timezone.now)

    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return self.used_point