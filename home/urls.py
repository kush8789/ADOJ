from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.home, name="home"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("problem/<int:pk>", views.problem, name="problem"),
    path("solution/<int:pk>", views.solution_code, name="solution"),
    # path("create/", views.problemform, name="problemform"),
    # path('problem/<int:pk>', views.problem, name='problem'),
]
