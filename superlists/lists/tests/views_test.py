import pytest
from django.urls import resolve
from pytest_django.asserts import assertTemplateUsed, assertRedirects

from ..views import home_page
from ..models import Item, List


TEXT = 'a new text'


@pytest.mark.django_db
class TestHomePage:
    @pytest.fixture()
    def response(self, client):
        return client.get('/')

    @pytest.fixture
    def post_res(self, client):
        response = client.post('/', data={'new_item': TEXT})
        return response

    def test_root_url_should_use_homepage_method(self):
        home = resolve('/')
        assert home.func == home_page, '应该用 home_page 方法'

    def test_get_homepage_should_return_200(self, response):
        assert response.status_code == 200, f'response的 code 是 {response.status_code}'

    def test_get_homepage_should_contain_今日清单(self, response):
        assert '今日清单' in response.content.decode(), '应该显示 今日清单'

    def test_use_correct_template(self, response):
        assertTemplateUsed(response, 'lists/home.html')


    def test_get_request_should_not_modify_db(self, client):
        client.get('/')

        assert Item.objects.count() == 0

@pytest.mark.django_db
class TestListView:
    def test_get_request_should_show_all_items_in_db(self, client):
        list_ = List.objects.create()
        Item.objects.create(text='item1', list=list_)
        Item.objects.create(text='item2', list=list_)

        response = client.get(f'/lists/{list_.id}/')

        assert 'item1' in response.content.decode()
        assert 'item2' in response.content.decode()

    def test_list_page_should_use_list_template(self, client):
        list_ = List.objects.create()
        other_list = List.objects.create()

        response = client.get(f'/lists/{list_.id}/')
        assertTemplateUsed(response, 'lists/list.html')
        assert response.context['list'] == list_

    def test_item_model_should_save_post_request_from_list_page(self, client):
        response = client.post('/lists/', data={'new_item': 'an item'})

        assert Item.objects.count() == 1

        new_item = Item.objects.first()
        assert new_item.text == 'an item'
    
    def test_list_page_should_show_only_items_from_one_list(self, client):
        one_list = List.objects.create()
        Item.objects.create(text='item1', list=one_list)
        Item.objects.create(text='item2', list=one_list)

        other_list = List.objects.create()
        Item.objects.create(text='other item1', list=other_list)
        Item.objects.create(text='other item2', list=other_list)

        get_response = client.get(f'/lists/{one_list.id}/')

        assert 'item1' in get_response.content.decode()
        assert 'item2' in get_response.content.decode()

        assert 'other item1' not in get_response.content.decode()
        assert 'other item2' not in get_response.content.decode()

@pytest.mark.django_db
class TestCreateItem:
    def test_create_item_to_correct_list(self, client):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        text = 'some random test'
        client.post(f'/lists/{correct_list.id}/items/', data={'new_item': text})

        assert Item.objects.count() == 1

        new_item = Item.objects.first()
        assert new_item.text == text

        assert new_item.list == correct_list

    def test_post_redirect_to_list_view(self, client):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        text = 'some random test'
        response = client.post(f'/lists/{correct_list.id}/items/', data={'new_item': text})

        assertRedirects(response, f'/lists/{correct_list.id}/')