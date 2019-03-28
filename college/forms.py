from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class StudentRegForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['usn', 'mobile', 'address', 'sem']


class MarksForm(forms.ModelForm):
    class Meta:
        model = Submarks
        fields = ['I', 'II', 'III', 'attendence']


class CreateSubmark(forms.ModelForm):
    class Meta:
        model = Submarks
        fields = ['student', 'subject', 'I', 'II', 'III']

class CreateBatch(forms.ModelForm):
    class Meta:
        model = BatchAdd
        fields = ['batch_name']




class AddAssignment(forms.ModelForm):
    class Meta:
        model = Assignments

        fields = ['title', 'assignment', 'deadline']
        widgets = {
            'deadline': forms.TextInput(
                attrs={'class': 'form-action', 'rows': 1, 'cols': 1, 'placeholder': 'eg:- Jan 21,2019'})}


class ReviewForm(forms.ModelForm):
    feedback = forms.Textarea(attrs={'class': 'form-action', 'row': 2, 'col': 2})

    class Meta:
        model = Review

        fields = ['professor', 'rating', 'feedback']
