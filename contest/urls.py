from django.urls import path
from . import views

app_name = "contest"

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>/", views.contest, name="contest"),
    path("<int:pk>/page/", views.contestpage, name="contestpage"),
    path("<int:pk1>/problem/<int:pk2>/", views.problem, name="problem"),
    path("<int:pk>/leaderboard/", views.leaderboard, name="contest_leaderboard"),
    path("<int:pk>/submissions/", views.submissions, name="contest_submissions"),
    path("<int:pk1>/solution/<int:pk2>", views.solution_code, name="solution"),
]
