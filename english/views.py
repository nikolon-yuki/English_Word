from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.http import QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import View
from django.db.models import Q
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from .models import Playlist, Card, Like
from accounts.models import CustomUser
from .forms import PlaylistForm, CardForm, SearchForm, DeeplForm
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import json
import requests
import deepl


SEARCH_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId=1036071663739197165"

translator = deepl.Translator("afcb9f3d-bd19-11ce-8aed-6b71bfb74e57:fx")



def get_api_data(params):
    api = requests.get(SEARCH_URL, params=params).text
    result = json.loads(api)
    items = result["Items"]
    return items


def deepl_data(keyword):
    result = translator.translate_text(keyword, target_lang="JA")
    return result


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = "english/playlist/create.html"
    form_class = PlaylistForm
    success_url = reverse_lazy("english:playlist_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = "english/playlist/list.html"


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "english/card/create.html"
    form_class = CardForm

    def get_success_url(self):
        return reverse_lazy("english:card_list", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    model = Playlist
    template_name = "english/playlist/delete.html"

    success_url = reverse_lazy("english:playlist_list")


@login_required
def card_list(request, pk):
    card_lis = Card.objects.filter(user=request.user)
    eng = request.GET.get("eng")

    if eng:
        card_lis = card_lis.filter(Q(word__icontains=eng))

    liked_list = []
    for card in card_lis:
        liked = card.like_set.filter(user=request.user)
        if liked.exists():
            liked_list.append(card.id)

    params = {
        "card_lis": card_lis,
        "liked_list": liked_list,
    }

    return render(request, "english/card/list.html", params)


@login_required
def likeview(request):
    if request.method == "POST":
        card = get_object_or_404(Card, pk=request.POST.get("card_id"))
        user = request.user
        liked = False
        like = Like.objects.filter(card=card, user=user)
        if like.exists():
            like.delete()
        else:
            like.create(card=card, user=user)
            liked = True

        params = {
            "card_id": card.id,
            "liked": liked,
            "count": card.like_set.count(),
        }
    if request.is_ajax():
        return JsonResponse(params)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        return render(request, "english/index.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        if form.is_valid():
            keyword = form.cleaned_data["title"]
            params = {
                "title": keyword,
                "hits": 30,
            }
            items = get_api_data(params)
            book_data = []
            for i in items:
                item = i["Item"]
                title = item["title"]
                image = item["largeImageUrl"]
                isbn = item["isbn"]
                query = {
                    "title": title,
                    "image": image,
                    "isbn": isbn,
                }
                book_data.append(query)

            return render(
                request,
                "english/search.html",
                {
                    "book_data": book_data,
                    "keyword": keyword,
                },
            )
        return render(request, "english/playlist/list.html", {"form": form})


class DetailView(View):
    def get(self, request, *args, **kwargs):
        isbn = self.kwargs["isbn"]
        params = {"isbn": isbn}

        items = get_api_data(params)
        items = items[0]
        item = items["Item"]
        title = item["title"]
        image = item["largeImageUrl"]
        itemPrice = item["itemPrice"]
        salesDate = item["salesDate"]
        publisherName = item["publisherName"]
        isbn = item["isbn"]
        itemUrl = item["itemUrl"]
        itemCaption = item["itemCaption"]

        book_data = {
            "title": title,
            "image": image,
            "itemPrice": itemPrice,
            "salesDate": salesDate,
            "publisherName": publisherName,
            "isbn": isbn,
            "itemUrl": itemUrl,
            "itemCaption": itemCaption,
        }

        return render(request, "english/detail.html", {"book_data": book_data})


class DeeplView(View):
    def get(self, request, *args, **kwargs):
        form = DeeplForm(request.POST or None)

        return render(request, "english/deepl.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = DeeplForm(request.POST or None)

        if form.is_valid():
            keyword = form.cleaned_data["text"]
            items = deepl_data(keyword)
            word_data = items.text

            return render(
                request,
                "english/result.html",
                {
                    "word_data": word_data,
                    "keyword": keyword,
                },
            )
        return render(request, "english/playlist/list.html", {"form": form})
