from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from . import views

urlpatterns=[
	url(r'^new/article$', views.new_article, name='new-article'),
    url(r'^$',views.news_today,name='newsToday'),
    url(r'^archives/(\d{4}-\d{2}-\d{2})/$',views.past_days_news,name = 'pastNews'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^article/(\d+)', views.article, name = 'article'),
    # url(r'^accounts/', include('registration.backends.simple.urls'), name='signup'),

]


#To serve uploaded images on the development server we need to configure our urls.py to register the MEDIA_ROOT route.
# add to the urlpatterns a new static route that references the location to the uploaded files.
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)