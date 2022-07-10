from django.urls import path

from recipes import views

app_name = "recipes"
urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name="home"),
    path('recipes/search', views.RecipeListViewSearch.as_view(),
         name='search'),
    path('category/<int:category_id>',
         views.RecipeListViewCategory.as_view(), name="category"),
    path('recipe/<int:pk>', views.RecipeDetails.as_view(),
         name="recipe")
]
