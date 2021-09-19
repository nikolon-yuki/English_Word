from django.urls import path

from . import views

app_name = 'english'

urlpatterns = [
    # path('',views.IndexView.as_view(),name='index'),
    path('playlist/create/',views.PlaylistCreateView.as_view(),name='playlist_create'),
    path('',views.PlaylistListView.as_view(),name='playlist_list'),
    path('card/create/',views.CardCreateView.as_view(),name='card_create'),
    path('card/list/<int:pk>/',views.card_list,name='card_list'),
]