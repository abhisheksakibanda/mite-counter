from django.urls import path

from . import views

app_name = 'growlivapp'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('upload-photos/', views.upload_photos, name='upload_photos'),
    path('instruction/', views.Instructions, name='instruction'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    # Add other URLs as needed
]
