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
    
    def clean(self):
        word = self.cleaned_data['word']
        card = Card.objects.filter(word=word).exists()
        if card:
            raise forms.ValidationError('すでに入力されています')

        return self.cleaned_data