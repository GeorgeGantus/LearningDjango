from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegisterForm


# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register.html', context={
        'form': form,
        'form_action': reverse('authors:create')})


def register_create(request):
    if not request.POST:
        raise Http404()
    post = request.POST
    request.session['register_form_data'] = post
    form = RegisterForm(post)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        form.save()
        messages.success(request, 'Author created')
        del(request.session['register_form_data'])
    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_action': reverse('authors:login_action')
    })


def login_action_view(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )
        if authenticated_user:
            messages.success(request, 'You are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        messages.error(request, 'Invalid username or password')
    return redirect('authors:dashboard')


@login_required(login_url='authors:login', redirect_field_name='redirect')
def logout_action_view(request):
    if not request.POST:
        raise Http404()
    if request.POST.get('username') == request.user.username:
        logout(request)
        messages.success(request, 'Logged out')
        return redirect('authors:login')
    messages.error(request, 'Invalid logout user')
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='redirect')
def dashboard_view(request):
    return render(request, 'authors/pages/dashboard.html')
