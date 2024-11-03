from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from .models import Recipe, Category

def home(request):
    context = {
        'recipes': Recipe.objects.filter(is_published=True).order_by('-id')
    }
    return render(request, 'recipes/pages/home.html', context)


def recipe(request, id):
    recipe = Recipe.objects.filter(id=id, is_published=True).first()
    context = {
        'recipe': recipe,
        'is_detail_page': True,
        'recipe_title': f'{recipe.title} - Recipe' if recipe else 'This recipe does not exist'
    }
    
    return render(request, 'recipes/pages/recipe-view.html', context)

def recipes_by_category(request, category_id):
    category = None
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        pass
    
    recipes = Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id')
    
    context = {
        'recipes': recipes,
        'category_exists': True if category else False,
        'category_name': f'{category.name} - Category' if category else 'This category does not exist'
    }
    
    return render(request, 'recipes/pages/category.html', context)

