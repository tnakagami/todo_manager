from django.urls import path
from . import views

app_name = 'todolist'

urlpatterns = [
    # top page
    path('', views.TopPage.as_view(), name='index'),
    # own task
    path('doing/', views.DoingTasks.as_view(), name='doing_task'),
    path('earned_point_history/', views.EarnedPointsHistory.as_view(), name='earned_point_history'),
    path('detail_doing/<int:pk>', views.DetailTask.as_view(template_name='todolist/detail_doing.html'), name='detail_doing'),
    path('detail_earned_point/<int:pk>', views.DetailTask.as_view(template_name='todolist/detail_earned_point.html'), name='detail_earned_point'),
    path('update/<int:pk>', views.UpdateTaskStatus.as_view(), name='update_task_status'),
    # create task
    path('create/task', views.CreateTask.as_view(), name='create_task'),
    path('create/task_category', views.CreateTaskCategory.as_view(), name='create_task_category'),
    # each user tasks
    path('each_user_tasks/', views.EachUserTaskPage.as_view(), name='each_user_tasks'),
]