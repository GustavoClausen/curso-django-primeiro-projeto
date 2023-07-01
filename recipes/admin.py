from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tag.models import Tag

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


class TagInline(GenericStackedInline):
    model = Tag
    fields = 'name',
    extra = 1


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
    prepopulated_fields = {
        'slug': ('title',)
    }

    inlines = [
        TagInline,
    ]


admin.site.register(Category, CategoryAdmin)
