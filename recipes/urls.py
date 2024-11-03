from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/<int:id>/', views.recipe, name='recipe'),
    path('recipes/category/<int:category_id>/', views.recipes_by_category, name='recipe-by-category')
]