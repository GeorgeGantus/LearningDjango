from django.urls import path

from recipes import views

app_name = "recipes"
urlpatterns = [
    path('', views.home, name="home"),
    path('recipes/search', views.search, name='search'),
    path('category/<int:category_id>', views.category, name="category"),
    path('recipe/<int:id>', views.recipe, name="recipe")
]
