from django.urls import path

from heroes import views


urlpatterns = [
    path('hero/', views.HeroAPIView.as_view(), name='hero')
]