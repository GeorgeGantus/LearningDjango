from django.shortcuts import render

from .models import Recipe


def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'recipes/pages/home.html',
                  context={'recipes': recipes})


def recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    return render(request, 'recipes/pages/recipe.html',
                  context={'recipe': recipe,
                           'is_detail_page': True})
