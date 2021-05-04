from django.urls import path
from . import views

app_name = 'todolist'

urlpatterns = [
    # top page
    path('', views.ToDoList.as_view(), name='index'),
    # own post
    path('detail/<int:pk>', views.DetailTask.as_view(), name='detail_task'),
    path('update/<int:pk>', views.UpdateTaskStatus.as_view(), name='update_task_status'),
]
