from django.contrib import admin
from .models import Card, Playlist, Like

# Register your models here.
admin.site.register(Card)
admin.site.register(Playlist)
admin.site.register(Like)
