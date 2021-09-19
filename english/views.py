from django.shortcuts import render,redirect,resolve_url,get_object_or_404
from django.urls import reverse_lazy
from django.http import QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import CreateView,DetailView,ListView
from .models import Playlist,Card
from accounts.models import CustomUser
from .forms import PlaylistForm,CardForm
# Create your views here.
# class IndexView(generic.TemplateView):
#     template_name='english/index.html'

class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'english/playlist/create.html'
    form_class = PlaylistForm
    success_url = reverse_lazy("english:playlist_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlaylistListView(LoginRequiredMixin,ListView):
    model = Playlist
    template_name = 'english/playlist/list.html'

class CardCreateView(LoginRequiredMixin,CreateView):
    model = Card
    template_name = 'english/card/create.html'
    form_class = CardForm

    def get_success_url(self):
        return reverse_lazy('english:card_list',kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def card_list(request,pk):
    card_lis = Card.objects.filter(user = request.user)
    playlist_lis = Playlist.objects.filter(user=request.user)

    values = request.POST.getlist('test')
    c_num = 0
    c_num_lis = []

    if not values == 0:
        c_num += 1
    else:
        pass
    c_num_lis.append(c_num)

    params = {
        'card_lis':card_lis,
        'c_num_lis':c_num_lis,
    }

    return render(request, 'english/card/list.html',params)
