import pytest

from ..models import Item

@pytest.mark.django_db
class TestItemModel:
    def test_can_save_and_retrive_items(self):
        first_text = 'first text'
        first_item = Item()
        first_item.text = first_text
        first_item.save()

        second_text = 'second text'
        second_item = Item()
        second_item.text = second_text
        second_item.save()

        save_items = Item.objects.all()
        assert save_items.count() == 2

        assert save_items[0].text == first_text
        assert save_items[1].text == second_text


        