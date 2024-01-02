from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

# Create your views here.


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
                return render(request, "priem/signupuser.html", {'form': UserCreationForm(), 'error':'Пароли не совпадают'})
        except IntegrityError:
            return render(request, "priem/signupuser.html",{'form': UserCreationForm(), 'error': 'Данный пользователь уже существует'})


def homepage(request):
    return render(request, "priem/homepage.html")
