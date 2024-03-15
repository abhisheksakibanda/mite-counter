from django.urls import path
from .views import signup, login, home, upload_photos, Instructions, profile, history

from . import views

app_name = 'growlivapp'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('upload-photos/', views.upload_photos, name='upload_photos'),
    path('instraction/', Instructions, name='instraction'),
    path('profile/', profile, name='profile'),
    path('history/', history, name='history'),
    # Add other URLs as needed
]
