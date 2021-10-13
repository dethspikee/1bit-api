from django.urls import path

from .views import home, upload_img


urlpatterns = [
    path('', home, name='home'),
    path('convert', upload_img),
]
