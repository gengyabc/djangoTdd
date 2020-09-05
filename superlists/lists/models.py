from django.db import models

class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey('List', default=None, on_delete=models.CASCADE)

class List(models.Model):
    pass
