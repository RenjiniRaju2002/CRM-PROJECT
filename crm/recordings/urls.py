from django.urls import path 
from .import views

urlpatterns=[
    path('recordings/',views.RecordingView.as_view(),name='recordings'),
]