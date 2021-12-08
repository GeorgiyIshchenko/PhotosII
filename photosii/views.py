from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from django.http import JsonResponse

from .models import *
from .forms import *


def homepage(request):
    search_query = request.GET.get('search', '').lower()
    if search_query:
        tags = Tag.objects.filter(name__icontains=search_query)
    else:
        tags = Tag.objects.all()
    tags = tags.order_by('name')
    return render(request, 'homepage.html', {'tags': tags, 'search_input': True})


def photo_view(request, id):
    photo = get_object_or_404(Photo, id=id)
    return render(request, 'photo_view.html', {'photo': photo})


def photo_add(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
    form = PhotoForm()
    return render(request, 'photo_add.html', {'form': form})
