import string
from random import SystemRandom

from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            random_tag = ''.join(
                SystemRandom().choices(string.ascii_letters + string.digits,
                                       k=5,)
            )
            self.slug = slugify(f'{self.name}-{random_tag}')
        super().save(*args, **kwargs)
