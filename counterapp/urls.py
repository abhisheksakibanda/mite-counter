from django.urls import path

from . import views

app_name = 'counterapp'

urlpatterns = [
    path('predict/<int:video_id>', views.predict, name='predict'),
]
