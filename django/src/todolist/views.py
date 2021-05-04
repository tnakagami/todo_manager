from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic import ListView, UpdateView, DetailView
from . import models, forms

User = get_user_model()

class ToDoList(LoginRequiredMixin, ListView):
    """
    ToDo list
    """
    raise_exception = True
    model = models.Task
    template_name = 'todolist/index.html'
    paginate_by = 10
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not (user.is_staff or user.is_superuser):
            queryset = queryset.filter(user=user)
        queryset = queryset.order_by('-created_at')

        return queryset

class DetailTask(AccessMixin, DetailView):
    raise_exception = True
    model = models.Task
    template_name = 'todolist/detail_task.html'

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
    success_url = reverse_lazy('todolist:index')

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
        task = form.save(commit=False)
        task.is_done = not task.is_done
        task.save()

        return super().form_valid(form)
