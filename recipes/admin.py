from django.contrib import admin
from .models import Category, Recipe

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Exibe o ID e o nome da categoria na lista
    search_fields = ('name',)  # Permite buscar categorias pelo nome
    ordering = ('name',)  # Ordena a lista pelo nome da categoria

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'is_published', 'created_at')  # Campos a serem exibidos na lista
    search_fields = ('title', 'description')  # Permite buscar receitas pelo título ou descrição
    list_filter = ('category', 'is_published')  # Adiciona filtros para a lista
    prepopulated_fields = {'slug': ('title',)}  # Preenche o campo slug com base no título
    ordering = ('-created_at',)  # Ordena a lista pela data de criação (mais recente primeiro)

# Registro dos modelos com suas classes admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
