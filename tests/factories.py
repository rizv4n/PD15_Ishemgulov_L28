import factory

from ads.models import Ad, Selection, Category
from authentication.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = "123qwe"
    role = "admin"
    age = 23
    birthday = "2020-05-23"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "test"
    slug = factory.Faker("name")


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = "test"
    author = factory.SubFactory(UserFactory)
    price = 100
    address = "test"
    category = factory.SubFactory(CategoryFactory)


class SelectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Selection

    name = "test"
    owner = 1
    items = 1
