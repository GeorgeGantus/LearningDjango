from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html',
                  context={'recipes': recipes})


def category(request, category_id):
    recipes_by_category = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/category.html',
                  context={'recipes': recipes_by_category,
                           'category_name': recipes_by_category[0]
                           .category.name})


def recipe(request, id):
    recipe = get_object_or_404(
        Recipe.objects.filter(id=id, is_published=True))
    return render(request, 'recipes/pages/recipe.html',
                  context={'recipe': recipe,
                           'is_detail_page': True})


def search(request):
    search = request.GET.get('q', '').strip()
    if not search:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(Q(title__icontains=search) | Q(description__icontains=search)),
        is_published=True

    )

    return render(request, 'recipes/pages/search.html', context={
        'search_value': search,
        'recipes': recipes
    })
