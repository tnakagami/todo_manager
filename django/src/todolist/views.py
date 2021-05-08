from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import date
from . import models, forms

User = get_user_model()

def paginate_query(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return paginator, page_obj

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
        queryset = super().get_queryset().filter(user=self.request.user, limit_date__gte=date.today())
        queryset = queryset.order_by('-pk')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        categories = models.TaskCategory.objects.all()
        category_pks = categories.values_list('pk', flat=True)
        context['categories'] = categories
        context['completed_count'] = {pk: qs.filter(category__pk=pk, is_done=True).count() for pk in category_pks}
        context['total_count'] = {pk: qs.filter(category__pk=pk).count() for pk in category_pks}

        return context

class EarnedPointsHistory(LoginRequiredMixin, ListView):
    """
    earned points history
    """
    raise_exception = True
    model = models.Task
    template_name = 'todolist/earned_point_history.html'
    paginate_by = 50
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user, is_done=True)
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
        # ・認証済みかつ、taskに登録されているユーザのpkが、リクエストしたユーザのpkと等しい
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
            task.update_complete_date()
            # ポイントを加算
            self.request.user.profile.update(task.point)
            self.request.user.profile.save()

        task.save()

        return HttpResponseRedirect(self.get_success_url())

class StaffUserMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 以下を満たすときにアクセスを許可
        # ・ユーザがログイン済みであるかつ、スタッフ権限を持つ
        user = self.request.user
        ret = user.is_authenticated and user.is_staff

        return ret

class TaskCategory(StaffUserMixin, ListView):
    model = models.TaskCategory
    template_name = 'todolist/task_category.html'
    context_object_name = 'categories'

class CreateTaskCategory(StaffUserMixin, CreateView):
    model = models.TaskCategory
    form_class = forms.TaskCategoryForm
    template_name = 'todolist/task_category_form.html'
    success_url = reverse_lazy('todolist:task_category')

class UpdateTaskCategory(StaffUserMixin, UpdateView):
    model = models.TaskCategory
    form_class = forms.TaskCategoryForm
    template_name = 'todolist/task_category_form.html'
    success_url = reverse_lazy('todolist:task_category')

class CreateTask(StaffUserMixin, CreateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'todolist/create_task_form.html'
    success_url = reverse_lazy('todolist:index')

class UpdateTask(StaffUserMixin, UpdateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'todolist/update_task_form.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = self.object.user
        context['target_user'] = user
        context['back_url'] = reverse('todolist:detail_user_tasks', kwargs={'pk': user.pk })

        return context

    def get_success_url(self):
        user = self.object.user
        return reverse('todolist:detail_user_tasks', kwargs={'pk': user.pk})

class EachUserPage(StaffUserMixin, ListView):
    raise_exception = True
    model = User
    template_name = 'todolist/each_user.html'
    paginate_by = 100
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_staff=False)
        form = forms.UserSearchForm(self.request.GET or None)
 
        # check form
        if form.is_valid():
            queryset = form.filtered_queryset(queryset)
        # ordering
        queryset = queryset.order_by('-pk')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = models.Task.objects.all()
        user_pks = self.get_queryset().values_list('pk', flat=True)
        context['search_form'] = forms.UserSearchForm(self.request.GET or None)
        context['completed_count'] = {pk: tasks.filter(user__pk=pk, is_done=True).count() for pk in user_pks}
        context['doing_count'] = {pk: tasks.filter(user__pk=pk, is_done=False).count() for pk in user_pks}

        return context

class DetailUserTaskPage(StaffUserMixin, DetailView):
    raise_exception = True
    model = User
    template_name = 'todolist/detail_user_tasks.html'
    context_object_name = 'target_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = models.Task.objects.filter(user__pk=self.kwargs['pk']).order_by('-pk')
        paginator, page_obj = paginate_query(self.request, tasks, 10)
        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return context
