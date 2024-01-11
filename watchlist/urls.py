from django.urls import path
from .import views

urlpatterns = [
    path('movie/', views.list_movies, name='movies'),
    path('movie/<int:page>/', views.list_movies, name='moviesi_with_page'),
    path('search/', views.search_movie, name='search'), 
]
