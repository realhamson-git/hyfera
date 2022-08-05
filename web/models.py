from django.db import models
from django.core.validators import EmailValidator
from django.urls import reverse
from django.template.defaultfilters import slugify
import requests
from django.conf import settings


# Create your models here.

class RequestMovieModel(models.Model):
    movieName = models.CharField(max_length = 500)
    email = models.EmailField(max_length = 100 , validators = [EmailValidator])
    def __str__(self):
        return self.movieName


class CategoryModel(models.Model):
    category = models.CharField(max_length = 50)
    def __str__(self):
        return f'{self.category} '

class TagsModel(models.Model):
    tags = models.CharField(max_length = 50)
    def __str__(self):
        return f'{self.tags} '
    
    def get_absolute_url(self):
        return reverse('tags-page', kwargs = {'tag':self.tags})


class CastModel(models.Model):
    actors = models.CharField(max_length = 100)
    def __str__(self):
        return f'{self.actors} '

class LanguageModel(models.Model):
    language = models.CharField(max_length = 10)
    def __str__(self):
        return f'{self.language}'

class MovieModel(models.Model):
    movie = models.CharField(max_length = 200)
    slug = models.SlugField(default = 'empty')
    image = models.URLField(max_length = 1000)
    description = models.TextField()
    language = models.ManyToManyField(LanguageModel)
    cast = models.ManyToManyField(CastModel)
    category = models.ForeignKey(CategoryModel, on_delete = models.DO_NOTHING)
    tags = models.ManyToManyField(TagsModel)
    release = models.DateField()
    def __str__(self):
        return self.movie
    
    def get_absolute_url(self):
        return reverse('movie-page',kwargs = {'slug':self.slug})

    def save(self, *args, **kwargs):
        self.movie = self.movie.capitalize()
        self.slug = slugify(self.movie)
        super(MovieModel, self).save(*args, **kwargs)
  


    
class ScreenshotsModel(models.Model):
    movie = models.ForeignKey(MovieModel, on_delete = models.CASCADE)
    screenshots = models.URLField(max_length = 1000)
    def __str__(self):
        moviename = MovieModel.objects.get(movie = self.movie)
        return moviename.movie


def latestMovie():
    return MovieModel.objects.last()
quality_choice = (('480px','480px'),('720px','720px'),('1080px','1080px'))

class UrlModel(models.Model):
    movie = models.ForeignKey(MovieModel, on_delete = models.CASCADE, default=latestMovie)
    quality = models.CharField(max_length = 10, choices = quality_choice, default = '480px')
    url = models.URLField(max_length = 1000000, blank = True, null = True)
    shrink_url = models.URLField(max_length = 10000, blank = True, null= True)

    def __str__(self):
        moviename = MovieModel.objects.get(movie = self.movie)
        return moviename.movie
    
    def save(self, *args, **kwargs):
        if(not self.shrink_url ):
            movieObj = MovieModel.objects.get(movie = self.movie)
            url = f'https://shrinkearn.com/api?api={ settings.SHRINK_API }&url={ self.url }&alias={ movieObj.slug[:23] }-{ self.quality }'
            req = requests.get(url)
            json = req.json()
            self.shrink_url = json['shortenedUrl']
            super(UrlModel, self).save(*args, **kwargs)
        super(UrlModel, self).save(*args, **kwargs)
        

    
