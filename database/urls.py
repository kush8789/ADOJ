from django.urls import path
from . import views
urlpatterns=[
    path('', views.home, name='home'),
    path('problem/<int:pk>', views.problem, name='problem'),
]