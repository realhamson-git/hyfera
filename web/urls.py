from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('movie-page/<slug:slug>', views.moviepage, name='movie-page'),
    path('request-page',views.requestPage, name = 'request-page'),
    path('tags/<str:tag>', views.tagspage, name = 'tags-page'),
    path('category/<str:category>', views.categorypage, name = 'categories-page'),
    path('language/<str:audio>', views.languagepage, name = 'language-page'),
    path('search', views.searchpage, name = 'search-page'),
]