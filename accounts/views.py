from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/register.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('main')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            # Invalid login
            return redirect('login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


register = RegisterView.as_view()
login_user = LoginView.as_view()
logout_user = LogoutView.as_view()