from django.db import models
from accounts.models import CustomUser

# Create your models here.


class Jojo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ("created_at",)
