from django.shortcuts import render,get_list_or_404
from django.http import HttpResponse
from.models import Problem,Solution,Testcase

# Create your views here.
def home(request):
    problems=Problem.objects.all()
    return render(request, 'home.html',{'problems': problems})

def problem(request,pk):
    if request.method=="POST":
        solution=request.POST["solution"]
        print(solution)
    problemOne=Problem.objects.filter(id=pk).values
    # print(problemOne)
    return render(request, 'problem.html',{'problem': problemOne})
    
    
