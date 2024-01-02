from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import SurveyForm


# Create your views here.
def mainpage(request):
    return render(request, 'priem/mainpage.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, "priem/signupuser.html", {'form': UserCreationForm()})
    else:  # == "POST"
        try:
            if request.POST['password1'] == request.POST['password2']:  # проверка на соответствие паролей
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('homepage')  # !!! Перенаправление на ниже созданное отображение
            else:
                return render(request, "priem/signupuser.html",
                              {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})
        except IntegrityError:
            return render(request, "priem/signupuser.html",
                          {'form': UserCreationForm(), 'error': 'Данный пользователь уже существует'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, "priem/loginuser.html", {'form': AuthenticationForm()})
    else:  # == "POST"
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "priem/signupuser.html",
                              {'form': AuthenticationForm(), 'error': 'Пароль пользователя неверный'})
        else:
            login(request, user)
            return redirect('homepage')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('mainpage')


def sendsurvey(request):
    if request.method == 'GET':
        return render(request, "priem/survey.html", {'form': SurveyForm()})
    else:
        pass


def homepage(request):
    return render(request, "priem/homepage.html")
