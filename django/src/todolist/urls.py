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
    # list task category
    path('task_category/', views.TaskCategory.as_view(), name='task_category'),
    # create task category
    path('task_category/create/', views.CreateTaskCategory.as_view(), name='create_task_category'),
    # update task category
    path('task_category/update/<int:pk>', views.UpdateTaskCategory.as_view(), name='update_task_category'),
    # create task
    path('task/create/', views.CreateTask.as_view(), name='create_task'),
    # update task
    path('task/update/<int:pk>', views.UpdateTask.as_view(), name='update_task'),
    # each user
    path('each_user/', views.EachUserPage.as_view(), name='each_user'),
    path('each_user/detail/<int:pk>', views.DetailUserTaskPage.as_view(), name='detail_user_tasks'),
]