from django import forms

from .models import Problem,Testcase,Solution

class ProblemForm(forms.ModelForm):
  class Meta:
      model=Problem
      fields=['statement','code','name','difficulty']
      widgets = {
            'statement': forms.Textarea(attrs={'class': 'form-control my-2', 'placeholder': 'Enter problem statement'},),
            'code': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter problem code'},),
            'name': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Problem name'},),
        }

class TestcaseForm(forms.ModelForm):
  class Meta:
      model=Testcase
      fields=['input','output']
      widgets = {
            'input': forms.Textarea(attrs={'class': 'form-control my-2', 'placeholder': 'Enter input'},),
            'output': forms.Textarea(attrs={'class': 'form-control my-2', 'placeholder': 'Enter output'},),
        }
      

class SolutionForm(forms.ModelForm):
  class Meta:
    model=Solution
    fields=['language','solution_code']
    widgets={
      'language':forms.Select(choices=(("C","c"),("C++","cpp"),("Python","py")),attrs={'class': 'form-control my-2',}),
      'solution_code': forms.Textarea(attrs={'class': 'form-control my-2 code-editor',}),
    }
    