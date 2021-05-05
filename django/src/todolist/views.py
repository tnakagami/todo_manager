from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from django.utils import timezone
from datetime import date
from . import models, forms

User = get_user_model()

class TopPage(LoginRequiredMixin, TemplateView):
    template_name = 'todolist/index.html'

class DoingTasks(LoginRequiredMixin, ListView):
    """
    Doing task list
    """
    raise_exception = True
    model = models.Task
    template_name = 'todolist/doing_tasks.html'
    paginate_by = 10
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        queryset = queryset.order_by('-pk')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.TaskCategory.objects.all()

        return context

class History(LoginRequiredMixin, ListView):
    """
    history
    """
    raise_exception = True
    model = models.Task
    template_name = 'todolist/history.html'
    paginate_by = 50
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user, complete_date__gte=date.today(), is_done=True)
        queryset = queryset.order_by('-complete_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()

        return context

class DetailTask(AccessMixin, DetailView):
    raise_exception = True
    model = models.Task

    def get_object(self, queryset=None):
        try:
            task = super().get_object(queryset=queryset)
        except Exception:
            raise Http404

        user = self.request.user
        allowed_user = user.is_staff or user.is_superuser
        matched_user = user.is_authenticated and user.pk == task.user.pk
        if matched_user or allowed_user:
            ret = task
        else:
            ret = self.handle_no_permission()

        return ret

class UpdateTaskStatus(AccessMixin, UpdateView):
    raise_exception = True
    model = models.Task
    form_class = forms.UpdateTaskStatus
    template_name = '404.html'
    success_url = reverse_lazy('todolist:doing_task')

    def get(self, request, *args, **kwargs):
        # ignore direct access
        return self.handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        try:
            task = self.model.objects.get(pk=kwargs['pk'])
        except Exception:
            raise Http404

        # 以下のいずれかを満たすときにアクセスを許可
        # ・スーパーユーザもしくはスタッフ権限を持つユーザ
        # ・認証済みかつ、taskのpkがユーザのpkと等しい
        user = request.user
        allowed_user = user.is_staff or user.is_superuser
        matched_user = user.is_authenticated and user.pk == task.user.pk
        if matched_user or allowed_user:
            response = super().dispatch(request, *args, **kwargs)
        else:
            response = self.handle_no_permission()

        return response

    def form_valid(self, form):
        task = self.model.objects.get(pk=self.kwargs['pk'])
        task.is_done = not task.is_done

        if task.is_done:
            # 完了時に完了日を更新
            task.complete_date = timezone.now()
            # ポイントを加算
            self.request.user.profile.score += task.point
            self.request.user.profile.achievements += 1
            self.request.user.profile.save()

        task.save()

        return HttpResponseRedirect(self.get_success_url())

class StaffUserMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        ret = user.is_authenticated and user.is_staff

        return ret

class CreateTaskCategory(StaffUserMixin, CreateView):
    model = models.TaskCategory
    form_class = forms.CreateTaskCategory
    template_name = 'todolist/create_task_category.html'
    success_url = reverse_lazy('todolist:index')

class CreateTask(StaffUserMixin, CreateView):
    model = models.Task
    form_class = forms.CreateTask
    template_name = 'todolist/create_task.html'
    success_url = reverse_lazy('todolist:index')

class EachUserTaskPage(StaffUserMixin, ListView):
    raise_exception = True
    model = models.Task
    template_name = 'todolist/each_user_tasks.html'
    paginate_by = 100
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = forms.UserSearchForm(self.request.GET or None)
 
        # check form
        if form.is_valid():
            queryset = form.filtered_queryset(queryset)
        # ordering
        queryset = queryset.order_by('-pk')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = forms.UserSearchForm(self.request.GET or None)

        return context
