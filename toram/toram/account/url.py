from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

app_name='account'
urlpatterns=[
    # path(r'register/', views.createuser, name='register'),
    path(r"register/", views.register, name="register"),
    path(r'login/', auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(), name="logout"),
]