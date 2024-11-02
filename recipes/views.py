from django.shortcuts import render
from utils.recipes.factory import make_recipe

def home(request):
    contexto = {
        'recipes': [make_recipe() for _ in range(10)]
    }
    return render(request, 'recipes/pages/home.html', context=contexto)


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html')
