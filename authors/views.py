from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import RegisterForm


# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register.html', context={
        'form': form})


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
