from django.contrib import admin
from .models import Contest, ContestProblem, ContestSolution, Leaderboard, ProblemStatus

# Register your models here.
admin.site.register(Contest)
admin.site.register(ContestProblem)
admin.site.register(ContestSolution)
admin.site.register(Leaderboard)
admin.site.register(ProblemStatus)
