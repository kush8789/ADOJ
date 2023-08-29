from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Contest, ContestProblem, Leaderboard, ContestSolution, ProblemStatus
from datetime import datetime, time
from home.models import Problem, Solution, Testcase
from django.contrib.auth.decorators import login_required
from home.forms import *
import docker
import subprocess
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages
from datetime import time


# from .forms import ContestSolutionForm


# Your other imports...


# Create your views here.
def home(request):
    try:
        upcoming_contests = Contest.objects.filter(
            contest_date__gte=datetime.today()
        ).order_by("contest_date", "start_time")

        previous_contests = Contest.objects.filter(
            contest_date__lte=datetime.today()
        ).order_by("-contest_date")

    except Contest.DoesNotExist:
        messages.error(
            request,
            "Please wait for new contest.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")
    return render(
        request,
        "contest/contestlinks.html",
        {
            "upcoming_contests": upcoming_contests,
            "previous_contests": previous_contests,
        },
    )


# @login_required
def contest(request, pk):
    # current_date = datetime.today().date()
    # contest_date = Contest.contest_date
    # if contest_date < current_date:
    #     messages.error(
    #         request,
    #         "Sorry, contest not started yet!!",
    #         extra_tags="alert alert-warning alert-dismissible fade show",
    #     )
    #     return redirect("contest:contestlinks.html")
    try:
        contest = get_object_or_404(Contest, pk=pk)
    except Contest.DoesNotExist:
        messages.error(
            request,
            "Contest does not exist.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")

    current_date = timezone.now().date()
    if current_date < contest.contest_date:
        return render(request, "contest/instructionpage.html", {"contest": contest})

    # current_datetime = timezone.now()
    current_datetime = timezone.now()

    # Check if the contest is live
    current_time = current_datetime.time()
    # Check if today is the contest day
    if (
        (current_date == contest.contest_date)
        and (contest.start_time <= current_time <= contest.end_time)
    ) or (current_date > contest.contest_date):
        return redirect("contest:contestpage", contest.pk)
    else:
        return render(request, "contest/instructionpage.html", {"contest": contest})


def get_submission_status(contest, user, problem_code):
    try:
        submission = ProblemStatus.objects.get(
            contest=contest, username=user, problem_code=problem_code
        )
        return submission.verdict
    except ProblemStatus.DoesNotExist:
        pass  # If no submission exists for the user and problem, return "Not Submitted"
    return ""


# Your other imports...


@login_required
def contestpage(request, pk):
    try:
        contest = get_object_or_404(Contest, pk=pk)
    except Contest.DoesNotExist:
        messages.error(
            request,
            "Contest does not exist.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")
    # Get all problems for the contest
    current_date = timezone.now().date()
    if current_date < contest.contest_date:
        return render(request, "contest/instructionpage.html", {"contest": contest})

    current_datetime = timezone.now()
    current_time = current_datetime.time()
    if (
        (current_date == contest.contest_date)
        and (contest.start_time <= current_time <= contest.end_time)
    ) or (current_date > contest.contest_date):
        # return redirect("contest:contestpage", contest.pk)
        pass
    else:
        return render(request, "contest/instructionpage.html", {"contest": contest})
    try:
        problems = ContestProblem.objects.filter(contest=contest)
    except ContestProblem.DoesNotExist:
        messages.error(
            request,
            "Oops!! please try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")

    contest_problems = []

    # Iterate over the problems and get the status for each
    for problem in problems:
        # Use ProblemStatus to get the submission status
        try:
            curr_problem = get_object_or_404(Problem, id=problem.problem.id)
            submission_status = ProblemStatus.objects.get(
                username=request.user, problem_code=curr_problem
            )
            status = submission_status.verdict
        except Problem.DoesNotExist:
            messages.error(
                request,
                "Problem does not exist.",
                extra_tags="alert alert-danger alert-dismissible fade show",
            )
            return redirect("contest:home")
        except ProblemStatus.DoesNotExist:
            status = ""
            messages.error(
                request,
                "Problem status does not exist, please try again.",
                extra_tags="alert alert-danger alert-dismissible fade show",
            )
            return redirect("contest_problems")

        contest_problems.append((curr_problem, status))

    return render(
        request,
        "contest/contestpage.html",
        {"contest": contest, "contest_problems": contest_problems},
    )


# Your other views...


def problem(request, pk1, pk2):
    try:
        contest = get_object_or_404(Contest, pk=pk1)
        problem = Problem.objects.get(id=pk2)
        testcase = Testcase.objects.get(problem=problem)
    except Contest.DoesNotExist:
        messages.error(
            request,
            "contest does not exist, please try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")
    except Problem.DoesNotExist:
        messages.error(
            request,
            "problem does not exist, please try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")
    except Testcase.DoesNotExist:
        messages.error(
            request,
            "testcase does not exist, please try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")

    # Check if the contest is live
    current_date = timezone.now().date()
    if current_date < contest.contest_date:
        return redirect("contest:home")

    current_datetime = timezone.now()
    current_time = current_datetime.time()
    if (current_date == contest.contest_date) and (
        contest.start_time <= current_time <= contest.end_time
    ):
        is_contest_live = True
    else:
        is_contest_live = False

    # Check if today is the contest day

    # if current_date == contest.contest_date:
    #     is_contest_day = True
    # else:
    #     is_contest_day = False

    # Check if the contest has ended
    if current_date > contest.contest_date:
        contest_has_ended = True
    else:
        contest_has_ended = False

    if request.method == "POST":
        if request.user.is_authenticated:
            if not is_contest_live and not contest_has_ended:
                # Contest has ended or today is not the contest day
                messages.error(
                    request,
                    "Solution submissions are not allowed at this time.",
                    extra_tags="alert alert-danger alert-dismissible fade show",
                )
                return redirect("contest:home")

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
            if is_contest_live:
                sol = ContestSolution()
            else:
                sol = Solution()

            # sol = ContestSolution()
            sol.contest = contest
            sol.username = request.user
            sol.problem_code = problem
            sol.language = language
            sol.solution_code = solution_code
            sol.verdict = output
            sol.save()

            #########NEW#########
            getstatus, createstatus = ProblemStatus.objects.get_or_create(
                username=request.user, problem_code=problem
            )

            if createstatus:
                getstatus.verdict = output
                getstatus.save()
                if getstatus.verdict == "AC":
                    try:
                        leaderboard, created = Leaderboard.objects.get_or_create(
                            username=request.user, contest=contest
                        )
                        leaderboard.score += 1
                        leaderboard.update = datetime.now()
                        leaderboard.save()
                    except Exception:
                        messages.error(
                            request,
                            "leaderboard not updated, please wait for some time.",
                            extra_tags="alert alert-danger alert-dismissible fade show",
                        )
            else:
                if getstatus.verdict == "AC":
                    pass
                else:
                    getstatus.verdict = output
                    getstatus.save()
                    if getstatus.verdict == "AC":
                        try:
                            leaderboard, created = Leaderboard.objects.get_or_create(
                                username=request.user, contest=contest
                            )
                            leaderboard.score += 1
                            leaderboard.update = datetime.now()
                            leaderboard.save()
                        except Exception:
                            messages.error(
                                request,
                                "leaderboard not updated, please wait for some time.",
                                extra_tags="alert alert-danger alert-dismissible fade show",
                            )
            #########NEW-END#########

        # Not loggedin
        else:
            return redirect("account:login")

    # Form
    solutionform = SolutionForm()
    solutionform.fields["language"].initial = "cpp"

    return render(
        request,
        "home/problem.html",
        {
            "problem": problem,
            "testcase": testcase,
            "solutionform": solutionform,
            # "status": status,
        },
    )
    # return render(request,'home/leaderboard.html',context)


@login_required
def leaderboard(request, pk):
    try:
        contest = get_object_or_404(Contest, pk=pk)
        leaderboard = Leaderboard.objects.filter(contest=contest).order_by(
            "score", "-update"
        )
    except Contest.DoesNotExist:
        messages.error(
            request,
            "contest does not exist, please try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")
    except Leaderboard.DoesNotExist:
        messages.error(
            request,
            "leaderboard not updated, please wait for some time.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")
    current_date = timezone.now().date()
    if current_date < contest.contest_date:
        return render(request, "contest/instructionpage.html", {"contest": contest})

    current_datetime = timezone.now()
    current_time = current_datetime.time()
    if (
        (current_date == contest.contest_date)
        and (contest.start_time <= current_time <= contest.end_time)
    ) or (current_date > contest.contest_date):
        # return redirect("contest:contestpage", contest.pk)
        pass
    else:
        return render(request, "contest/instructionpage.html", {"contest": contest})

    # print(leaderboard)
    return render(
        request,
        "contest/contestpage.html",
        {"contest": contest, "leaderboard": leaderboard},
    )


@login_required
def submissions(request, pk):
    try:
        contest = get_object_or_404(Contest, pk=pk)
        print(contest)
        submissions = ContestSolution.objects.filter(
            contest=contest, username=request.user
        )
        print(submissions)
    except Contest.DoesNotExist:
        messages.error(
            request,
            "contest does not exist, please try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:home")
    except ContestSolution.DoesNotExist:
        messages.error(
            request,
            "solution does not exist, wait for some time.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:contestpage")
    current_date = timezone.now().date()
    if current_date < contest.contest_date:
        return render(request, "contest/instructionpage.html", {"contest": contest})

    current_datetime = timezone.now()
    current_time = current_datetime.time()
    if (
        (current_date == contest.contest_date)
        and (contest.start_time <= current_time <= contest.end_time)
    ) or (current_date > contest.contest_date):
        # return redirect("contest:contestpage", contest.pk)
        pass
    else:
        return render(request, "contest/instructionpage.html", {"contest": contest})
    return render(
        request,
        "contest/contestpage.html",
        {"contest": contest, "submissions": submissions},
    )


def solution_code(request, pk1, pk2):
    try:
        solution = ContestSolution.objects.filter(id=pk2).values()
    except Solution.DoesNotExist:
        messages.error(
            request,
            "solution does not exist, try again.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("home:leaderboard")

    try:
        solution = solution[0]
        problem = Problem.objects.get(pk=solution["problem_code_id"])
        # problem = Problem.objects.filter(pk=solution['problem_code_id'])
        # if problem.live:
        #     messages.error(
        #         request,
        #         "Sorry you can't see contest solution.",
        #         extra_tags="alert alert-danger alert-dismissible fade show",
        #     )
        #     return redirect("home:home")
    except Problem.DoesNotExist:
        messages.error(
            request,
            "Problem does not exist.",
            extra_tags="alert alert-danger alert-dismissible fade show",
        )
        return redirect("contest:contestpage")

    return render(request, "solution/code.html", {"solution": solution})


##########################################################
###########@@DUMP-AREA@@##################################
##########################################################


# def contestpage(request, pk):
#     contest = get_object_or_404(Contest, pk=pk)

#     # Create a QuerySet to get all of the problems for the contest.
#     problems = ContestProblem.objects.filter(contest=contest)
#     print(problems)


#     contest_problems = []

#     for problem in problems:
#         curr_pr =  get_object_or_404(Problem, id=problem.problem.id)
#         contest_problems.append(curr_pr)

#     for pr in contest_problems:
#         print(pr)

#     print(contest_problems)
#     return render(
#         request,
#         "contest/contestpage.html",
#         {"contest": contest, "contest_problems": contest_problems},
#     )


# # @login_required
# def contest(request, pk):
#     # current_date = datetime.today().date()
#     # contest_date = Contest.contest_date
#     # if contest_date < current_date:
#     #     messages.error(
#     #         request,
#     #         "Sorry, contest not started yet!!",
#     #         extra_tags="alert alert-warning alert-dismissible fade show",
#     #     )
#     #     return redirect("contest:contestlinks.html")
#     try:
#         contest = get_object_or_404(Contest, pk=pk)
#     except Contest.DoesNotExist:
#         messages.error(
#             request,
#             "Contest does not exist.",
#             extra_tags="alert alert-danger alert-dismissible fade show",
#         )
#         return redirect("contest:home")

#     current_date = timezone.now().date()
#     if current_date < contest.contest_date:
#         return render(request, "contest/instructionpage.html")

#     current_datetime = timezone.now()
#     if contest.start_time <= current_datetime <= contest.end_time:
#         is_contest_live = True
#     else:
#         is_contest_live = False

#     # Check if today is the contest day
#     if current_date == contest.contest_date:
#         is_contest_day = True
#     else:
#         is_contest_day = False

#     # Check if the contest has ended
#     if (is_contest_day and is_contest_live) or (current_datetime > contest.contest_date):
#         # contest_has_ended = True
#         return redirect("contest:contestpage")
#     else:
#         contest_has_ended = False
#     context = {
#         "contest": contest,
#     }

#     return render(request, "contest/instructionpage.html", context)


# # @login_required
# def contest2(request, pk):
#     # current_date = datetime.today().date()
#     # contest_date = Contest.contest_date
#     # if contest_date < current_date:
#     #     messages.error(
#     #         request,
#     #         "Sorry, contest not started yet!!",
#     #         extra_tags="alert alert-warning alert-dismissible fade show",
#     #     )
#     #     return redirect("contest:contestlinks.html")
#     try:
#         contest = get_object_or_404(Contest, pk=pk)
#     except Contest.DoesNotExist:
#         messages.error(
#             request,
#             "Contest does not exist.",
#             extra_tags="alert alert-danger alert-dismissible fade show",
#         )
#         return redirect("contest:home")

#     context = {
#         "contest": contest,
#     }

#     return render(request, "contest/instructionpage.html", context)
