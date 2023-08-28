from django.db import models
from home.models import Problem
from django.contrib.auth.models import User


class Contest(models.Model):
    name = models.CharField(max_length=50, default="")
    contest_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Contest on {self.contest_date}"

    class Meta:
        ordering = ["contest_date", "start_time"]


class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Contest Problem: {self.problem} (Contest: {self.contest})"


class ContestSolution(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, default=None)
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    problem_code = models.ForeignKey(Problem, on_delete=models.CASCADE, default=None)
    language = models.CharField(
        max_length=7,
        choices=(("c", "C"), ("cpp", "C++"), ("py", "Python"), ("java", "Java")),
    )
    solution_code = models.TextField()
    verdict = models.CharField(max_length=50)
    submittedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.problem_code}"


class Leaderboard(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, default=None)
    score = models.PositiveIntegerField(default=0)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username.username}-{self.score}"


class ProblemStatus(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    problem_code = models.ForeignKey(Problem, on_delete=models.CASCADE, default=None)
    verdict = models.CharField(max_length=10, default="")

    def __str__(self):
        return f"{self.username.username}-{self.problem_code.code}-{self.verdict}"
