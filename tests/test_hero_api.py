import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from heroes.models import HeroModel


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def hero_data():
    return {
        'name': 'Batman',
        'intellegence': 0,
        'strength': 40,
        'speed': 29,
        'power': 63
    }


@pytest.fixture
def hero_instance(hero_data):
    return HeroModel.objects.create(**hero_data)


@pytest.mark.django_db
def test_get_all_heroes(api_client, hero_instance):
    response = api_client.get('/hero/')
    assert response.status_code == status.HTTP_200_OK
    assert any(hero['name'] == hero_instance.name for hero in response.json())


@pytest.mark.django_db
def test_get_hero_by_name(api_client, hero_instance):
    response = api_client.get('/hero/?name=Batman')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['name'] == 'Batman'


@pytest.mark.django_db
def test_get_hero_with_filter(api_client, hero_instance):
    response = api_client.get('/hero/?strength=40')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['strength'] == 40


@pytest.mark.django_db
def test_get_hero_not_found(api_client):
    response = api_client.get('/hero/?name=UnknowHero')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'error' in response.json()


@pytest.mark.django_db
def test_post_created_hero(api_client):
    response = api_client.post('/hero/', {'name': 'Batman'})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['strength'] == 40


@pytest.mark.django_db
def test_post_hero_already_exists(api_client, hero_instance):
    response = api_client.post('/hero/', {'name': 'Batman'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['detail'] == 'Hero already exists'


@pytest.mark.django_db
def test_post_hero_without_name(api_client):
    response = api_client.post('/hero/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == 'Name is required'
