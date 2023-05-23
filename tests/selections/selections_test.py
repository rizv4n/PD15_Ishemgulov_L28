import pytest

from ads.serializers import AdListSerializer
from authentication.models import User
from tests.factories import AdFactory, UserFactory


# @pytest.mark.django_db
# def test_ad_retrieve(client, ad, category, user, get_token):
#     expected_response = {
#         "id": ad.pk,
#         "name": "test",
#         "author": user.pk,
#         "price": 100,
#         "description": None,
#         "address": "test",
#         "category": category.pk,
#         "is_published": False,
#         "image": None
#     }
#
#     response = client.get(
#         f"/ad/{ad.id}/",
#         HTTP_AUTHORIZATION="Token " + get_token
#     )
#
#     assert response.status_code == 200
#     assert response.data == expected_response
#
#
# @pytest.mark.django_db
# def test_ad_list(client, get_token):
#     ads = AdFactory.create_batch(10)
#
#     expected_response = {
#         "count": 10,
#         "next": None,
#         "previous": None,
#         "results": AdListSerializer(ads, many=True).data
#     }
#
#     response = client.get("/ad/")
#
#     assert response.status_code == 200
#     assert response.data == expected_response


@pytest.mark.django_db
def test_selection_create(client, get_token):

    ads = AdFactory.create_batch(3)
    ads_list = AdListSerializer(ads, many=True).data
    items = [i["id"] for i in ads_list]

    data = {
        "name": "test_selection",
        "items": items
    }

    expected_response = {
        "name": "test_selection",
        "items": items
    }

    response = client.post(
        f"/selection/create/",
        data=data,
        data_format='json',
        HTTP_AUTHORIZATION="Token " + get_token
    )

    del response.data['id']
    del response.data['owner']

    assert response.status_code == 201
    assert response.data == expected_response
