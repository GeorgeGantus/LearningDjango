import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    tags = models.ManyToManyField(Tag, blank=True, default='')

    @staticmethod
    def resize_image(image, new_width=800):
        image_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height)/original_width)
        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_path,
            optimize=True,
            quality=50,
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        saved = super().save()

        if self.cover:
            self.resize_image(self.cover)

        return saved

    def get_absolute_url(self):
        return reverse("recipes:recipe", args=(self.id,))
