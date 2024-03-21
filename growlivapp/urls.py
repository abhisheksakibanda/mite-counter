from django.urls import path

from . import views

app_name = 'growlivapp'

urlpatterns = [
    # path for the home page
    path('', views.home, name='home'),

    # path for the login and registration pages
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),

    path('upload-photos/', views.upload_photos, name='upload_photos'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('scan_detail/', views.scan_detail_page, name='scan_detail_page'),

    # path for login related pages
    path('instruction/', views.Instructions, name='instruction'),
]
