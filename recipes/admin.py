from django.contrib import admin

from .models import Category, Recipe

# both ways do the same thing


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...

# End - Examples
