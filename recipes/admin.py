from django.contrib import admin

from .models import Category, Recipe

# both ways do the same thing


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'user')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'description', 'preparation_steps', 'slug')
    list_filter = ('category', 'user', 'is_published',
                   'preparation_steps_is_html')
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = ('-id',)
    prepopulated_fields = {
        'slug': ('title',)
    }

# End - Examples
