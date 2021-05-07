from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # Top Page
    path('', views.TopPage.as_view(), name='index'),
    # Login, Logout
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
    # user profile
    path('profile/', views.UserProfilePage.as_view(), name='user_profile'),
    # user list
    path('user/list', views.RegisteredUserPage.as_view(), name='registered_user'),
    # create user
    path('user/create', views.CreateUserPage.as_view(), name='create_user'),
    # update user profile
    path('user/update/<int:pk>', views.UpdateUserProfilePage.as_view(), name='update_user_profile'),
    # set password
    path('user/set_password/<int:pk>', views.SetPasswordPage.as_view(), name='set_password'),
]