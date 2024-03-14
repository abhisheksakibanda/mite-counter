# GrowLivApp/urls.py
from django.urls import path
from .views import signup, login, home, upload_photos

app_name = 'GrowLivApp'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('home/', home, name='home'),
    path('upload-photos/', upload_photos, name='upload_photos'),
    # Add other URLs as needed
]
