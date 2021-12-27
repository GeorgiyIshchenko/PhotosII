from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework import status
from django.http import JsonResponse

from .models import *
from .forms import *
from .serializers import *


def homepage(request):
    search_query = request.GET.get('search', '').lower()
    user_photos = Photo.objects.filter(user=request.user)
    if search_query:
        tags = Tag.objects.filter(name__icontains=search_query)
    else:
        tags = Tag.objects.filter()
    data = dict.fromkeys([tags[i].name for i in range(tags.count())], [])
    for tag in tags:
        data[tag.name] = user_photos.filter(tag=tag)
    print(data)
    return render(request, 'homepage.html', {'data': data, 'search_input': True})


def photo_view(request, id):
    photo = get_object_or_404(Photo, id=id)
    return render(request, 'photo_view.html', {'photo': photo})


def photo_add(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('/')
        else:
            print(form.errors)
    form = PhotoForm()
    return render(request, 'photo_add.html', {'form': form})


class PhotoListView(APIView):

    def get(self, request):
        photos = Photo.objects.all()
        serializer = PhotoListSerializer(photos, many=True)
        return Response(serializer.data)


class PhotoView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)

    def get(self, request, pk):
        photo = Photo.objects.get(id=pk)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)


class PhotoPost(APIView):

    def post(self, request):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
