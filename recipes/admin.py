from django.contrib import admin

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at', 'id')
    list_display_links = ['title']
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps'
    list_filter = [
        'category', 'author', 'is_published', 'preparation_steps_is_html'
    ]
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',


admin.site.register(Category, CategoryAdmin)
