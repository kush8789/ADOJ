from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.create_user, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
