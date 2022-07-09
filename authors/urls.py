from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),
    path('login/', views.login_view, name='login'),
    path('login/action/', views.login_action_view, name='login_action'),
    path('logout', views.logout_action_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/recipe/create/', views.DashboardRecipe.as_view(),
         name='dashboard_recipe_create'),
    path('dashboard/recipe/<int:id>/edit/',
         views.DashboardRecipe.as_view(), name='dashboard_recipe_edit'),
    path('dashboard/recipe/<int:id>/delete/',
         views.DashboardRecipeDelete.as_view(),
         name='dashboard_recipe_delete'),

]
