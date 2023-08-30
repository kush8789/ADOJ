from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# from djrichtextfield.models import RichTextField


# Create your models here.
class Problem(models.Model):
    # statement=models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    statement = RichTextField(blank=True, null=True)
    input_formate = RichTextField(blank=True, null=True)
    output_formate = RichTextField(blank=True, null=True)
    problem_constraint = RichTextField(blank=True, null=True)
    difficulty = models.CharField(
        max_length=10,
        choices=(("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")),
    )
    live = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class Solution(models.Model):
    username = models.ForeignKey(
        User, max_length=50, on_delete=models.CASCADE, default=None
    )
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


class Testcase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.TextField(default="", max_length=1000)
    output = models.TextField(default="", max_length=1000)

    def __str__(self):
        return self.problem.code
