from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control my-1", "placeholder": "Email"}
        ),
    )
    username = forms.CharField(
        label="Username",
        max_length=100,
        min_length=5,
        widget=forms.TextInput(attrs={"class": "form-control my-1"}),
    )
    password1 = forms.CharField(
        label="Password",
        max_length=50,
        min_length=5,
        widget=forms.PasswordInput(attrs={"class": "form-control my-1"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        max_length=50,
        min_length=5,
        widget=forms.PasswordInput(attrs={"class": "form-control my-1"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# class SignupForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=100, min_length=5,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label='Email', max_length=254, min_length=5,
#                              widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(label='Password', max_length=50, min_length=5,
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label='Confirm Password',
#                                 max_length=50, min_length=5,
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
