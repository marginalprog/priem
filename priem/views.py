from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import SurveyForm
from .models import Survey


# Create your views here.
def mainpage(request):
    if request.user.is_authenticated:
        try:  # Если объект в модели (запись) были созданы ранее, то выполняем код
            obj = Survey.objects.get(user=request.user)
            # Объект существует
            if obj.is_form_filled:
                if obj.worker:
                    return redirect('listabiture')
                else:
                    return redirect('homepage')
        except Survey.DoesNotExist:  # Если анкету не заполняли - перенаправление на форму
            return redirect('sendsurvey')
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
                        return redirect('listabiture')
                    else:
                        return redirect('homepage')
            except Survey.DoesNotExist:  # Если анкету не заполняли - перенаправление на форму
                return redirect('sendsurvey')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('mainpage')


@login_required
def sendsurvey(request):
    if request.method == 'GET':
        try:  # Если объект в модели (запись) были созданы ранее, то выполняем код
            obj = Survey.objects.get(user=request.user)
            if obj.is_form_filled:
                if obj.worker:
                    return redirect('listabiture')
                else:
                    return redirect('homepage')
        except Survey.DoesNotExist:
            return render(request, "priem/survey.html", {'form': SurveyForm()})
    else:
        try:
            form = SurveyForm(request.POST)
            newsurvey = form.save(commit=False)
            newsurvey.user = request.user
            newsurvey.save()
            if form.cleaned_data.get('worker'):  # Если работник комиссии
                return redirect('listabiture')
            else:
                return redirect('homepage')
        except ValueError:
            return render(request, 'priem/survey.html', {'form': SurveyForm(), 'error': 'Введены некорректные данные'})


@login_required
def listabiture(request):
    # query_surveys = Survey.objects.filter(worker=False)
    query_surveys = Survey.objects.select_related('user').filter(worker=False)
    return render(request, "priem/listabiture.html", {'query_surveys': query_surveys})


@login_required
def homepage(request):
    return render(request, "priem/homepage.html")
