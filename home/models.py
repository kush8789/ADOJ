from django.db import models

# Create your models here.
class Problem(models.Model):
    statement=models.CharField(max_length=255)
    name=models.CharField(max_length=50)
    code=models.CharField(max_length=50)
    difficulty=models.CharField(max_length=10, choices=(("Easy","easy"),("Medium","medium"),("Hard","hard")))
    
    def __str__(self):
        return self.name
        
class Solution(models.Model):
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    verdict=models.CharField(max_length=50)
    submittedAt=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.problem
    
class Testcase(models.Model):
    input=models.CharField(max_length=50)
    output=models.CharField(max_length=50)
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.input
    