from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')

def view_list(request, id):
    list_ = List.objects.get(id=id)
    items = Item.objects.filter(list=list_)
    return render(request, 'lists/list.html', {'list': list_})

def lists(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        text = request.POST['new_item']
        Item.objects.create(text=text, list=list_)
        return redirect(f'/lists/{list_.id}/')

def items(request, id):
    if request.method == 'POST':
        list_ = List.objects.get(id=id)
        text = request.POST['new_item']
        Item.objects.create(text=text, list=list_)
        return redirect(f'/lists/{list_.id}/')
