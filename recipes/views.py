import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import DetailView, ListView
from utils.pagination import make_pagination

from .models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, paginator_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE
        )
        context.update(
            {'recipes': page_obj, 'paginator_range': paginator_range}
        )
        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            category__id=self.kwargs.get('category_id')
        )
        if not queryset:
            raise Http404()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {'category_name': context.get('recipes')[0].category.name})
        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        search = self.request.GET.get('q', '')
        if not search:
            raise Http404()
        queryset = queryset.filter(
            Q(Q(title__icontains=search) | Q(description__icontains=search)),
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        search = self.request.GET.get('q', '')
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {'search_value': search,
             'additional_url_query': f'&q={search}'}
        )
        return context


class RecipeDetails(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_detail_page"] = True
        return context


# Keep here to have an example of function based views
""" def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, paginator_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/home.html',
                  context={
                      'recipes': page_obj,
                      'paginator_range': paginator_range
                  })


def category(request, category_id):
    recipes_by_category = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    page_obj, paginator_range = make_pagination(
        request, recipes_by_category, PER_PAGE)

    return render(request, 'recipes/pages/category.html',
                  context={'recipes': page_obj,
                           'category_name': recipes_by_category[0]
                           .category.name,
                           'paginator_range': paginator_range})


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
    ).order_by('-id')

    page_obj, paginator_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', context={
        'search_value': search,
        'recipes': page_obj,
        'paginator_range': paginator_range,
        'additional_url_query': f'&q={search}'
    }) """
