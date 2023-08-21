from django.urls import path
from . import views

app_name="problempg"


urlpatterns=[
    path('leaderboard/',views.leaderboard,name="leaderboard"),
    path('problem/<int:pk>', views.problem, name='problem'),
    path('create/',views.problemform,name="problemform"),
    path('solution/<int:pk>',views.solution_code,name="solution"),
]