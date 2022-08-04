from django.contrib import admin
from .models import RequestMovieModel, CategoryModel, CastModel, TagsModel, LanguageModel,MovieModel,ScreenshotsModel, UrlModel
from django.apps import apps
# Register your models here.

@admin.register(ScreenshotsModel)
class ScreenshotsModelAdmin(admin.ModelAdmin):
    list_display = ['movie','screenshots']
    search_fields = ['movie__movie']

@admin.register(MovieModel)
class MovieModelAdmin(admin.ModelAdmin):
    exclude = ['slug']
    date_hierarchy = 'release'
    list_display = ['id', 'movie', 'category', 'release', 'slug']
    search_fields = ['id', 'movie', 'category__category', 'release','tags__tags','cast__actors','language__language']


@admin.register(UrlModel)
class UrlModelAdmin(admin.ModelAdmin):
    search_fields = ['movie__movie','shrink_url']
    list_display = ['movie','quality','shrink_url']
    exclude = ['shrink_url']

model_list = [RequestMovieModel, CategoryModel, CastModel, TagsModel, LanguageModel]
for model in model_list:
    admin.site.register(model)


admin.site.site_header = 'Hyfera'
admin.site.index_title = 'hyfera admin'
