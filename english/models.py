from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Playlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created_at',)

class Card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=None)
    word = models.CharField(max_length=30)
    ja_word = models.CharField(max_length=100)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ('created_at',)


