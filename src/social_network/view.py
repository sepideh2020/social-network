from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView



def home_view(request):
    user = request.user
    hello = 'Hello'

    context = {
        'user': user,
        'hello': hello,
    }
    return render(request, 'main/home.html', context)


