from django.urls import path
from . import views

app_name = "mainapp"

urlpatterns = [
	path('', views.main, name = "main"),
	path('search/',views.search),
	path('movie/<str:id>/',views.movie_details, name = "movie")
]