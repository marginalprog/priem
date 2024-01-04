from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.utils.http import urlencode

from .forms import SurveyForm
from .models import Survey


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
            try:  # Если объект в модели (запись) были созданы ранее, то выполняем код
                obj = Survey.objects.get(user=request.user)
                # Объект существует
                if obj.is_form_filled:
                    if obj.worker:
                        return redirect('mainpage')
                    else:
                        return redirect('homepage')
            except Survey.DoesNotExist:  # Если анкету не заполняли - перенаправление на форму
                return redirect('sendsurvey')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('mainpage')


def sendsurvey(request):
    if request.method == 'GET':
        return render(request, "priem/survey.html", {'form': SurveyForm()})
    else:
        try:
            form = SurveyForm(request.POST)
            newsurvey = form.save(commit=False)
            newsurvey.user = request.user
            newsurvey.save()
            if form.cleaned_data.get('worker'):  # Если работник комиссии
                return redirect('mainpage')
            else:
                return redirect('mainpage')
        except ValueError:
            return render(request, 'priem/survey.html', {'form': SurveyForm(), 'error': 'Введены некорректные данные'})


def homepage(request):
    return render(request, "priem/homepage.html")
