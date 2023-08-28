from django.shortcuts import render, redirect
from .models import Problem, Solution, Testcase
from django.contrib.auth.decorators import login_required
from home.forms import *
import docker
import subprocess
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def home(request):
    try:
        problems = Problem.objects.filter(live=False)
    except Problem.DoesNotExist:
        messages.error(
            request,
            "Problem does not exist.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("home:home")
    difficulty = request.GET.get("difficulty", "all")
    if difficulty != "all":
        problems = problems.filter(difficulty=difficulty)

    return render(request, "home/home.html", {"problems": problems})


# Create your views here.
# @login_required
def problem(request, pk):
    try:
        problem = Problem.objects.get(id=pk)
    except Problem.DoesNotExist:
        messages.error(
            request,
            "Problem does not exist.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("home:home")
    if problem.live:
        return redirect("home:home")
    testcase = Testcase.objects.get(problem=problem)

    if request.method == "POST":
        if request.user.is_authenticated:
            language = request.POST.get("language", None)
            # print(language)
            solution_code = request.POST.get("solution_code", None)
            # print(solution_code)
            solutioncode = solution_code.replace("\r\n", "\n").strip()
            # print(solution_code)
            lang = str(language)
            # print(lang)

            testcase.output = testcase.output.replace("\r\n", "\n").strip()
            # print(testcase.output)
            # print(testcase.input)
            testcase_input = bytes(testcase.input, "utf-8")
            output = "WA"
            lang = ""
            res = ""

            docinit = docker.from_env()
            Running = "running"

            if language == "py":
                filepath = settings.FILES_DIR + "/pythoncode.py"
                py_code = open(filepath, "w")
                py_code.write(solutioncode)
                py_code.close()
                ##
                # container = docinit.containers.get("oj-py")
                # print(container)
                # container_state = container.attrs["State"]
                # print(container_state)

                try:
                    container = docinit.containers.get("oj-py")
                    # print(container)
                    container_state = container.attrs["State"]
                    # print(container_state)
                    container_is_running = container_state["Status"] == Running
                    if not container_is_running:
                        subprocess.run(["docker", "start", "oj-py"], shell=False)
                except docker.errors.NotFound:
                    subprocess.run(
                        ["docker", "run", "-dt", "--name", "oj-py", "python"],
                        shell=False,
                    )
                # copy/paste the .py file in docker container
                subprocess.run(["docker", "cp", filepath, "oj-py:/pythoncode.py"])
                # interpreting and running the code on given input and taking the output in a variable in bytes
                res = subprocess.run(
                    ["docker", "exec", "-i", "oj-py", "python", "pythoncode.py"],
                    input=testcase_input,
                    capture_output=True,
                    shell=False,
                )
                # removing the .py file form the docker container
                subprocess.run(
                    ["docker", "exec", "oj-py", "rm", "pythoncode.py"], shell=False
                )
                # checking if the code have errors
                if res.stderr.decode("utf-8") != "":
                    output = "CE"

                ##############CPP##############
            elif language == "cpp":
                filepath = settings.FILES_DIR + "/cppcode.cpp"
                cpp_code = open(filepath, "w")
                cpp_code.write(solutioncode)
                cpp_code.close()

                # checking if the docker container is running or not
                try:
                    container = docinit.containers.get("oj-cpp")
                    container_state = container.attrs["State"]
                    container_is_running = container_state["Status"] == Running
                    if not container_is_running:
                        subprocess.run(["docker", "start", "oj-cpp"], shell=False)
                except docker.errors.NotFound:
                    subprocess.run(
                        ["docker", "run", "-dt", "--name", "oj-cpp", "gcc"], shell=False
                    )

                # copy/paste the .cpp file in docker container
                subprocess.run(["docker", "cp", filepath, "oj-cpp:/cppcode.cpp"])
                # compiling the code
                res = subprocess.run(
                    ["docker", "exec", "oj-cpp", "g++", "-o", "output", "cppcode.cpp"],
                    capture_output=True,
                    shell=False,
                )
                # checking if the code have errors
                if res.stderr.decode("utf-8") != "":
                    output = "CE"
                # running the code on given input and taking the output in a variable in bytes
                res = subprocess.run(
                    ["docker", "exec", "-i", "oj-cpp", "./output"],
                    input=testcase_input,
                    capture_output=True,
                    shell=False,
                )
                # removing the .cpp and .output file form the container
                subprocess.run(["docker", "exec", "oj-cpp", "rm", "cppcode.cpp"])
                subprocess.run(["docker", "exec", "oj-cpp", "rm", "output"])

                ##############C##############
            elif language == "c":
                filepath = settings.FILES_DIR + "/ccode.c"
                c_code = open(filepath, "w")
                c_code.write(solutioncode)
                c_code.close()

                try:
                    container = docinit.containers.get("oj-c")
                    container_state = container.attrs["State"]
                    container_is_running = container_state["Status"] == Running
                    if not container_is_running:
                        subprocess.run(["docker", "start", "oj-c"], shell=False)
                except docker.errors.NotFound:
                    subprocess.run(
                        ["docker", "run", "-dt", "--name", "oj-c", "gcc"], shell=False
                    )

                subprocess.run(["docker", "cp", filepath, "oj-c:/ccode.c"], shell=False)
                res = subprocess.run(
                    ["docker", "exec", "oj-c", "gcc", "-o", "output", "ccode.c"],
                    capture_output=True,
                    shell=False,
                )
                if res.stderr.decode("utf-8") != "":
                    output = "CE"
                res = subprocess.run(
                    ["docker", "exec", "-i", "oj-c", "./output"],
                    input=testcase_input,
                    capture_output=True,
                    shell=False,
                )
                subprocess.run(["docker", "exec", "oj-c", "rm", "ccode.c"])
                subprocess.run(["docker", "exec", "oj-c", "rm", "output"])

            ###########After Compilation##########
            res = res.stdout.decode(
                "utf-8"
            )  # converting the res variable from bytes to string
            # print(res)
            if str(res) == str(testcase.output):
                output = "AC"
            testcase.output += "\n"  # added extra line to compare user output having extra ling at the end of their output
            if str(res) == str(testcase.output):
                output = "AC"

            ####Verdict#####
            # print(output)
            sol = Solution()
            # user = User.objects.get(username=request.user)
            sol.username = request.user
            sol.problem_code = problem
            sol.language = language
            sol.solution_code = solution_code
            sol.verdict = output
            sol.save()

        # Not loggedin
        else:
            return redirect("account:login")

    # Form
    solutionform = SolutionForm()
    solutionform.fields["language"].initial = "cpp"

    return render(
        request,
        "home/problem.html",
        {"problem": problem, "testcase": testcase, "solutionform": solutionform},
    )
    # return render(request,'home/leaderboard.html',context)


# @login_required
def leaderboard(request):
    try:
        allsub = request.GET.get("all", None)
        if request.user.is_authenticated:
            solutions = Solution.objects.filter(username=request.user)
            messages.error(
                request,
                "Please login to see submissions.",
                extra_tags="alert alert-danger alert-dismissible fade show",
            )
        else:
            allsub = "True"
        if allsub == "True":
            solutions = Solution.objects.all()
        solutions = solutions.order_by("-submittedAt")
    except Solution.DoesNotExist:
        messages.error(
            request,
            "solution does not exist, try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("leaderboard")
        # print(solutions)
        # for sol in solutions:
        #     print(sol)
    return render(request, "home/leaderboard.html", {"solutions": solutions})


# def problemform(request):
#     form = ProblemForm()
#     return render(
#         request,
#         "home/forms.html",
#         {
#             "form": form,
#         },
#     )


def solution_code(request, pk):
    try:
        solution = Solution.objects.filter(id=pk).values()
    except Solution.DoesNotExist:
        messages.error(
            request,
            "solution does not exist, try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("home:leaderboard")

    try:
        solution = solution[0]
        problem = Problem.objects.get(pk=solution['problem_code_id'])
        # problem = Problem.objects.filter(pk=solution['problem_code_id'])
        if problem.live:
            messages.error(
                request,
                "Sorry you can't see contest solution.",
                extra_tags="alert alert-danger alert-dismissible fade show",
            )
            return redirect("home:home")
    except Problem.DoesNotExist:
        messages.error(
            request,
            "Problem does not exist.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("home:home")

    return render(request, "solution/code.html", {"solution": solution})
