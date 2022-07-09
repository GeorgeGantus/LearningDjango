from authors.forms import AuthorRecipeForm, LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse
from recipes.models import Recipe


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
    recipes = Recipe.objects.filter(is_published=False, user=request.user)
    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': recipes
        }
    )


@login_required(login_url='authors:login', redirect_field_name='redirect')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        user=request.user,
        pk=id
    ).first()
    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.user = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()
        messages.success(request, "Recipe edited successfully")
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form
        }
    )


@login_required(login_url='authors:login', redirect_field_name='redirect')
def dashboard_recipe_create(request):

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.user = request.user
        recipe.is_published = False
        recipe.preparation_steps_is_html = False
        recipe.slug = slugify(recipe.title)

        recipe.save()
        messages.success(request, 'Recipe created successfully')
        return redirect(reverse('authors:dashboard_recipe_edit',
                                args=(recipe.id,)))

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form
        }
    )


@login_required(login_url='authors:login', redirect_field_name='redirect')
def dashboard_recipe_delete(request, id):
    if request.method != 'POST':
        raise Http404()
    recipe = Recipe.objects.filter(
        is_published=False,
        user=request.user,
        pk=id
    ).first()

    if not recipe:
        raise Http404()

    recipe.delete()
    messages.success(request, 'Recipe deleted')
    return redirect('authors:dashboard')
