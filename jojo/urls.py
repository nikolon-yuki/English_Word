from django.urls import path

from . import views

app_name = "jojo"

urlpatterns = [path("jojo/list/", views.jojo_change, name="jojo_list")]
