from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Item


def home_page(request):
    if request.method == 'POST':
        item = Item()
        item.text = request.POST['new_item']
        item.save()
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})
