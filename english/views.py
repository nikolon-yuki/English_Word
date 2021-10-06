from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.http import QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db.models import Q
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from .models import Playlist, Card, Like
from accounts.models import CustomUser
from .forms import PlaylistForm, CardForm
from django.http import JsonResponse, HttpResponse


# Create your views here.
# class IndexView(generic.TemplateView):
#     template_name='english/index.html'


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

    # def post(self, request):
    #     card_lis = Card.objects.filter(user=request.user)
    #     form = self.form_class(request.POST)
    #     form.instance.user = self.request.user
    #     for card in card_lis:
    #         if form.instance.word == card.word:
    #             card.count += 1
    #             card.save()
    #             return redirect("english:card_list", pk=card.pk)
    #         elif card.word != form.instance.word:
    #             context = get_success_url(self)
    #             return context


class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "english/card/delete.html"

    def get_success_url(self):
        return reverse_lazy("english:card_list", kwargs={"pk": self.object.pk})


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
