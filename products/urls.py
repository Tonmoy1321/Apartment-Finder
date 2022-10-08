from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('matches/', views.search, name='search'),
    path('mapview/', views.mapview, name='mapview'),
    path('postad', views.postadvert, name='postad'),
    path('profile', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('login', views.loginpage, name='login'),
    path('logout', views.logoutuser, name='logout'),
    path('bookmark/<int:id>/', views.add_bookmark, name='add_bookmark'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('error_occured/', views.handler404, name='error')
]
