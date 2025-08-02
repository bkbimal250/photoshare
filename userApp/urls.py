from django.urls import path
from . import views

app_name = 'userApp'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('photos/', views.photo_list, name='photo_list'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    
    # Photo management
    path('photo/upload/', views.photo_upload, name='photo_upload'),
    path('photo/<int:photo_id>/edit/', views.photo_edit, name='photo_edit'),
    path('photo/<int:photo_id>/delete/', views.photo_delete, name='photo_delete'),
    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),
    
    # User profile URLs
    path('profile/edit/', views.profile_edit, name='profile_edit'), # Moved this line up
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/photos/', views.user_photos, name='user_photos'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    
    # Albums
    path('albums/', views.album_list, name='album_list'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('album/create/', views.album_create, name='album_create'),
    
    # Categories
    path('category/<int:category_id>/', views.category_photos, name='category_photos'),
    
    # Search
    path('search/', views.search_results, name='search_results'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    
    # Sitemap
    path('sitemap/', views.sitemap, name='sitemap'),
    
    # SEO URLs
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
