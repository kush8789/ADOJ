from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from .models import Problem, Solution, Testcase


# Create your views here.
def home(request):
    problems = Problem.objects.all()
    difficulty = request.GET.get("difficulty", "all")
    if difficulty != "all":
        problems = problems.filter(difficulty=difficulty)

    return render(request, "home/home.html", {"problems": problems})
