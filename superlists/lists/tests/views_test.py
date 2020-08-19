import pytest
from django.urls import resolve
from pytest_django.asserts import assertTemplateUsed

from ..views import home_page
from ..models import Item


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

    # def test_handle_post_request(self, post_res):
    #     assert TEXT in post_res.content.decode()
    #     assertTemplateUsed(post_res, 'lists/home.html')

    def test_post_request_should_save_to_db(self, post_res):
        assert Item.objects.count() == 1

        new_item = Item.objects.first()
        assert new_item.text == TEXT

    def test_get_request_should_not_modify_db(self, client):
        client.get('/')

        assert Item.objects.count() == 0

    def test_post_request_should_redirect(self, post_res):
        assert post_res.status_code == 302
        assert post_res['location'] == '/'


    def test_get_request_should_show_all_items_in_db(self, client):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = client.get('/')

        assert 'item1' in response.content.decode()
        assert 'item1' in response.content.decode()

