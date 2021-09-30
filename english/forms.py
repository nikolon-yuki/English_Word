from django import forms
from .models import Playlist, Card


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ("title",)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = (
            "word",
            "ja_word",
            "playlist",
        )
