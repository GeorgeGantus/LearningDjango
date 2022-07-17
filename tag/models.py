import string
from random import SystemRandom

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Here start the generic relation fields

    # This field represens the model that will be acoplated ehre
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # this field represent the objects'id of the model above
    # is a charfield because the model can have an uuid pk
    object_id = models.CharField(max_length=255)

    # tell django that both field above are from a generic relashioship
    # its not necessary because we used the default names but to make it
    # explicit i will link them here to make it expliocit
    cotent_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            random_tag = ''.join(
                SystemRandom().choices(string.ascii_letters + string.digits,
                                       k=5,)
            )
            self.slug = slugify(f'{self.name}-{random_tag}')
        super().save(*args, **kwargs)
