from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # Top Page
    path('', views.TopPage.as_view(), name='index'),
    # Login, Logout
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
    # create user
    path('create_user/', views.CreateUserPage.as_view(), name='create_user'),
]