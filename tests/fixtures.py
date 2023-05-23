import pytest


@pytest.fixture()
@pytest.mark.django_db
def get_token(client, django_user_model):
    username = "Test_User"
    password = "123qwe"
    role = "admin"
    age = 23
    birthday = "2020-05-23"

    django_user_model.objects.create_user(
        username=username,
        password=password,
        role=role,
        age=age,
        birthday=birthday
    )

    response = client.post(
        "/user/login/",
        {"username": username, "password": password},
        format='json'
    )

    return response.data["token"]


