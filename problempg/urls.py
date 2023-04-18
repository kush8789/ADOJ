from django.urls import path
from . import views
urlpatterns=[
    path('problem/<int:pk>', views.problem, name='problem'),
]