from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = "blog"
urlpatterns = [
    path(
        r'',
        views.IndexView.as_view(),
        name='index'),
    path(
        r'page/<int:page>/',
        views.IndexView.as_view(),
        name='index_page'),
    path(
        r'article/<int:year>/<int:month>/<int:day>/<int:article_id>.html',
        views.ArticleDetailView.as_view(),
        name='detailbyid'),
    path(
        r'category/<slug:category_name>.html',
        views.CategoryDetailView.as_view(),
        name='category_detail'),
    path(
        r'category/<slug:category_name>/<int:page>.html',
        views.CategoryDetailView.as_view(),
        name='category_detail_page'),
    path(
        r'author/<author_name>.html',
        views.AuthorDetailView.as_view(),
        name='author_detail'),
    path(
        r'author/<author_name>/<int:page>.html',
        views.AuthorDetailView.as_view(),
        name='author_detail_page'),
    path(
        r'tag/<slug:tag_name>.html',
        views.TagDetailView.as_view(),
        name='tag_detail'),
    path(
        r'tag/<slug:tag_name>/<int:page>.html',
        views.TagDetailView.as_view(),
        name='tag_detail_page'),
    path(
        'archives.html',
        cache_page(
            60 * 60)(
            views.ArchivesView.as_view()),
        name='archives'),
    path(
        'links.html',
        views.LinkListView.as_view(),
        name='links'),
    path(
        r'upload',
        views.fileupload,
        name='upload'),
    path(
        r'clean',
        views.clean_cache_view,
        name='clean'),
    path(
        'big_screen.html',
        views.BigScreenView.as_view(),
        name='big_screen'),
    path(
        'bigscreen1/',
        views.BigScreen1View.as_view(),
        name='big_screen1'),
    path(
        'bigscreen2/',
        views.BigScreen2View.as_view(),
        name='big_screen2'),
    path(
        'bigscreen3/',
        views.BigScreen3View.as_view(),
        name='big_screen3'),
    path(
        'bigscreen4/',
        views.BigScreen4View.as_view(),
        name='big_screen4'),
]
