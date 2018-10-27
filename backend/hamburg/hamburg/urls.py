"""hamburg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from hamburg_api import views

# pylint: disable=invalid-name
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/v1/moviedb/search/$', views.SearchView.as_view()),
    re_path(r'^api/v1/alerts/save/$', views.EmailAlertView.as_view()),
    re_path(r'^api/v1/schedules/email/$', views.ScheduleRunView.as_view()),
    re_path(r'^api/v1/moviedb/details/$', views.MovieDetailsView.as_view()),
    re_path(r'^api/v1/moviedb/showtimes/$', views.ShowtimeDetailsView.as_view()),
    re_path(r'^api/v1/moviedb/upcoming/$', views.UpcomingView.as_view()),
    re_path(r'^api/v1/moviedb/popular/$', views.PopularView.as_view()),
    re_path(r'^api/v1/moviedb/now_playing/$', views.NowPlayingView.as_view()),
    re_path(r'^api/v1/moviedb/similar/$', views.SimilarView.as_view()),
    re_path(r'^api/v1/moviedb/recommended/$', views.RecommendedView.as_view()),
]
