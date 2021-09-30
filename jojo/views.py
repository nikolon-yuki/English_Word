from django.shortcuts import render
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from itertools import permutations
from .models import Jojo


# Create your views here.
def jojo_change(request):
    keyword = request.GET.get("keyword")
    subword = request.GET.get("subword")
    results = []
    subs = []
    for x in permutations([a for a in keyword]):
        results.append(''.join(x))

    params = {
        "results": results,
    }

    return render(request, "jojo/list.html", params)
