from django.urls import path

from .views import home_page, view_list, lists, items


urlpatterns = [
    path('', home_page, name='home'),
    path('lists/<int:id>/', view_list, name='view_list'),
    path('lists/<int:id>/items/', items, name='view_list'),
    path('lists/', lists, name='lists'),
]


