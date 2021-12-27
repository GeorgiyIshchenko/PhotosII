from django.urls import path, include
from django.conf.urls.static import static

from .views import *
from .apps import PhotosiiConfig

app_name = PhotosiiConfig.name

urlpatterns = [
    path('account/', include('account.urls')),
    path('', homepage, name='homepage'),
    path('photo_add', photo_add, name='photo_add'),
    path('<int:id>/', photo_view, name='photo_view'),
    path('api/photos', PhotoListView.as_view()),
    path('api/photos/<int:pk>', PhotoView.as_view()),
    path('api/photos/post', PhotoPost.as_view(),)
]
