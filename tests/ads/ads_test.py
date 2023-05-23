import pytest

from ads.serializers import AdListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_retrieve(client, ad, category, user, get_token):
    expected_response = {
        "id": ad.pk,
        "name": "test",
        "author": user.pk,
        "price": 100,
        "description": None,
        "address": "test",
        "category": category.pk,
        "is_published": False,
        "image": None
    }

    response = client.get(
        f"/ad/{ad.id}/",
        HTTP_AUTHORIZATION="Token " + get_token
    )

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_ad_list(client, get_token):
    ads = AdFactory.create_batch(10)

    expected_response = {
        "count": 10,
        "next": None,
        "previous": None,
        "results": AdListSerializer(ads, many=True).data
    }

    response = client.get("/ad/")

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_ad_create(client, category, get_token):

    data = {
        "name": "test_for_create",
        "price": 100,
        "address": "London",
        "category": category.pk,
    }

    expected_response = {
        "name": "test_for_create",
        "price": 100,
        "description": None,
        "address": "London",
        "category": category.pk,
        "is_published": False,
        "image": None
    }

    response = client.post(
        f"/ad/create/",
        data=data,
        data_format='json',
        HTTP_AUTHORIZATION="Token " + get_token
    )

    del response.data['id']
    del response.data['author']

    assert response.status_code == 201
    assert response.data == expected_response
