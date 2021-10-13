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
            "memo",
            "playlist",
        )

    def clean(self):
        word = self.cleaned_data["word"]
        card = Card.objects.filter(word=word).exists()
        if card:
            raise forms.ValidationError("すでに入力されています")

        return self.cleaned_data


class SearchForm(forms.Form):
    title = forms.CharField(label="書籍名", max_length=200, required=True)


class DeeplForm(forms.Form):
    text = forms.CharField(
        label="word",
        max_length=200,
        required=True,
        widget=forms.Textarea(attrs={"cols": "80", "rows": "10"}),
    )
