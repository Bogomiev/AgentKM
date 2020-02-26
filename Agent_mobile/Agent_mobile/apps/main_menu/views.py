from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib import messages

from django.template.context_processors import csrf


def index(request):
    context = {
        'agent': auth.get_user(request).username
    }
    return render(request, 'main_menu/homePage.html', context)


def login(request):
    args = {}
    args.update(csrf(request))
    # error_messages = ['args: '+"args", 'username: '+username, 'password: '+password]
    # messages.error(request, error_messages)
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            error_messages = ['args: ' + args['login_error'], 'username: ' + username, 'password: ' + password]
            messages.error(request, error_messages)
            return render(request, 'main_menu/homePage.html', args)

    else:
        return render(request, 'main_menu/homePage.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")
