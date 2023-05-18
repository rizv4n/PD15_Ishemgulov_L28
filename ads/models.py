from django.db import models

from authentication.models import User


class Ad(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=200)
    category = models.ForeignKey('ads.Category', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='ad_image', blank=True, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Selection(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Ad)
