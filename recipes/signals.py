from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category, Recipe

# Signals of Recipe
@receiver(post_save, sender=Recipe)
def clear_cache_on_recipe_save(sender, instance, **kwargs):
    cache.clear()
    
@receiver(post_delete, sender=Recipe)
def clear_cache_on_recipe_delete(sender, instance, **kwargs):
    cache.clear()

# Signals of Category 
@receiver(post_save, sender=Category)
def clear_cache_on_category_save(sender, instance, **kwargs):
    cache.clear()

@receiver(post_delete, sender=Category)
def clear_cache_on_category_delete(sender, instance, **kwargs):
    cache.clear()


