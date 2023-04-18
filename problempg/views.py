from django.shortcuts import redirect, render
from django.http import HttpResponse
from home.models import Problem,Solution,Testcase
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def problem(request,pk):
    if request.method=="POST":
        if request.user.is_authenticated:
            solution=request.POST["solution"]
            print(solution)
        else:
            return redirect('account:login')
    problemOne=Problem.objects.filter(id=pk).values
    # print(problemOne)
    return render(request, 'problempg/problem.html',{'problem': problemOne})
    