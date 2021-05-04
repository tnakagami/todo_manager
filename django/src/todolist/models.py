from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy
from django.core.validators import MinValueValidator

User = get_user_model()

class Task(models.Model):
    # user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # タスクのタイトル
    title = models.CharField(ugettext_lazy('title'), max_length=64)
    # タスクの内容
    text = models.TextField(ugettext_lazy('detail'))
    # タスクの状態
    is_done = models.BooleanField(ugettext_lazy('doing or done'), default=False)
    # タスク完了時の得点
    point = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    # タスク実施日時
    target_date = models.DateTimeField(ugettext_lazy('target date'), default=timezone.now)
    # 作成日時
    created_at = models.DateTimeField(ugettext_lazy('create time'), default=timezone.now)
    # 更新日時
    updated_at = models.DateTimeField(ugettext_lazy('update time'), default=timezone.now)

    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return self.title
