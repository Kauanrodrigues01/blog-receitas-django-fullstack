from django.shortcuts import render
from .models import Recipe, Category
from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
from decouple import config
from django.contrib.messages import error, success, info, debug, warning


RECIPES_PER_PAGE = config('RECIPES_PER_PAGE', cast=int)

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    
    page_obj, pagination_range = make_pagination(request, recipes, RECIPES_PER_PAGE)
    
    context = {
        'recipes': page_obj,
        'pagination_range': pagination_range,
    }
    
    error(request, 'QUE LEGAL FOI UM ERRO')
    
    return render(request, 'recipes/pages/home.html', context)


def recipe(request, id):
    recipe = Recipe.objects.filter(id=id, is_published=True).first()
    context = {
        'recipe': recipe,
        'is_detail_page': True,
        'recipe_title': f'{recipe.title} - Recipe' if recipe else 'This recipe does not exist'
    }
    
    if recipe:
        return render(request, 'recipes/pages/recipe-view.html', context)
    
    # cache.clear()
    return render(request, 'recipes/pages/recipe-view.html', context, status=404)

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
    
    if context['category_exists']:
        return render(request, 'recipes/pages/category.html', context)
    
    # cache.clear()
    return render(request, 'recipes/pages/category.html', context, status=404)


def search(request):
    search_term = request.GET.get('q', '').strip()
    
    if not search_term:
        raise Http404()
    
    context = {
        'search_term': search_term,
        'page_title': f'Search for "{search_term}" | Recipes',
        'recipes': Recipe.objects.filter(
                Q(
                    Q(title__icontains=search_term) | 
                    Q(description__icontains=search_term) | 
                    Q(preparation_steps__icontains=search_term)
                ) &
                Q(is_published=True)
                ).order_by('-id')
    }
    
    return render(request, 'recipes/pages/search.html', context)