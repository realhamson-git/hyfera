from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CategoryModel, TagsModel, MovieModel, CategoryModel, ScreenshotsModel, CastModel, RequestMovieModel, LanguageModel, UrlModel
from django.db.models import Q
from django.core.paginator import Paginator

# initailize model objects
category = CategoryModel.objects
tags = TagsModel.objects
movies = MovieModel.objects
categories = CategoryModel.objects
screenshots = ScreenshotsModel.objects
cast = CastModel.objects
language = LanguageModel.objects
urls = UrlModel.objects
allTags = tags.all()


# Create your views here.
def index(request):
    allMovies = movies.all().order_by('-id')
    p = Paginator(allMovies,per_page = 24, orphans = 2) 
    page_number = request.GET.get('page')
    try:
        page_obj = p.page(page_number)
    except:
        page_obj = p.page(1) 

    context = {'alltags':allTags,'latest':allMovies[:6],'allmovies':page_obj,'last_page':p}
    return render(request, 'index.html', context)

def moviepage(request, slug): 
    singlemovie = movies.get(slug = slug)
    cat_related = movies.filter(category = singlemovie.category)
    lan_related = movies.filter(language = singlemovie.language.first())
    relatedmovies = cat_related.union(lan_related)
    screen = screenshots.filter(movie = singlemovie)
    links = urls.filter(movie = singlemovie)
    casts = singlemovie.cast.all()
    return render(request, 'movie-page.html', {'alltags':allTags, 'singlemovie':singlemovie,'screenshot':screen,'links':links,'casts':casts,'relatedmovies':relatedmovies[:6]}) 



def tagspage(request, tag):
    print(tag, category)
    tagObj = tags.get(tags = tag)
    allmovies = movies.filter(tags = tagObj.id).order_by('movie')
    p = Paginator(allmovies,per_page = 7, orphans = 2) 
    page_number = request.GET.get('page')
    try:
        page_obj = p.page(page_number)
    except:
        page_obj = p.page(1)
    return render(request, 'tags-page.html', {'alltags':allTags,'allmovies':page_obj,'last_page':p})

def categorypage(request, category):
    categoryObj = categories.get(category = category)
    allmovies = movies.filter(category = categoryObj.id).order_by('movie')
    p = Paginator(allmovies,per_page = 7, orphans = 2) 
    page_number = request.GET.get('page')
    try:
        page_obj = p.page(page_number)
    except:
        page_obj = p.page(1)
    return render(request, 'category-page.html', {'alltags':allTags,'allmovies':page_obj,'last_page':p})

def languagepage(request, audio):
    Obj = language.get(language = audio)
    allmovies = movies.filter(language = Obj.id).order_by('movie')
    p = Paginator(allmovies,per_page = 7, orphans = 2) 
    page_number = request.GET.get('page')
    try:
        page_obj = p.page(page_number)
    except:
        page_obj = p.page(1)
    return render(request, 'language-page.html', {'alltags':allTags,'allmovies':page_obj,'last_page':p})

def searchpage(request):
    query = request.GET.get('q')
    allmovies = movies.filter(Q(movie__icontains = query))
    p = Paginator(allmovies,per_page = 7, orphans = 2) 
    page_number = request.GET.get('page')
    try:
        page_obj = p.page(page_number)
    except:
        page_obj = p.page(1)
    return render(request, 'search-page.html', {'alltags':allTags,'allmovies':page_obj,'last_page':p})

def requestPage(request):
    if(request.method == 'POST'):
        movie = request.POST.get('movie')
        email = request.POST.get('email')
        reqObj = RequestMovieModel(movieName = movie, email = email).save()
        return redirect('/')
    return HttpResponse('Sorry something went wrong')