from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.template.loader import render_to_string
from .models import CustomUser, Photo, Album, Category, Comment, Follow
from .forms import PhotoUploadForm, AlbumForm, UserProfileForm, CommentForm, CustomUserCreationForm
import json

def home(request):
    """Home page with featured photos and recent uploads"""
    featured_photos = Photo.objects.filter(is_public=True).order_by('-views', '-created_at')[:12]
    recent_photos = Photo.objects.filter(is_public=True).order_by('-created_at')[:8]
    categories = Category.objects.annotate(photo_count=Count('photos')).order_by('-photo_count')[:6]
    
    # SEO context
    seo_context = {
        'meta_title': 'PhotoShare - Share Your Photography with the World',
        'meta_description': 'Join PhotoShare, the premier photography community. Upload, share, and discover stunning photos from photographers worldwide. Connect with fellow artists and showcase your creative vision.',
        'meta_keywords': 'photography, photo sharing, photographers, photo community, photo upload, photo gallery, photography platform, photo showcase, photo portfolio, photo art',
        'og_title': 'PhotoShare - Share Your Photography with the World',
        'og_description': 'Join PhotoShare, the premier photography community. Upload, share, and discover stunning photos from photographers worldwide.',
        'og_type': 'website',
        'twitter_title': 'PhotoShare - Share Your Photography with the World',
        'twitter_description': 'Join PhotoShare, the premier photography community. Upload, share, and discover stunning photos from photographers worldwide.',
        'schema_type': 'WebSite',
    }
    
    context = {
        'featured_photos': featured_photos,
        'recent_photos': recent_photos,
        'categories': categories,
        **seo_context,
    }
    return render(request, 'userApp/home.html', context)

def photo_list(request):
    """Display all public photos with filtering and pagination"""
    photos = Photo.objects.filter(is_public=True)
    
    # Filtering
    category_id = request.GET.get('category')
    if category_id:
        photos = photos.filter(category_id=category_id)
    
    search_query = request.GET.get('search')
    if search_query:
        photos = photos.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query) |
            Q(photographer__username__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        photos = photos.order_by('created_at')
    elif sort_by == 'popular':
        photos = photos.order_by('-views', '-likes__count')
    elif sort_by == 'liked':
        photos = photos.order_by('-likes__count', '-created_at')
    else:  # newest
        photos = photos.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(photos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    # SEO context
    seo_context = {
        'meta_title': 'Photo Gallery - Browse Amazing Photography | PhotoShare',
        'meta_description': 'Browse thousands of amazing photos from talented photographers worldwide. Discover stunning photography in various categories and styles.',
        'meta_keywords': 'photo gallery, photography, photos, image gallery, photo collection, photography showcase',
        'og_title': 'Photo Gallery - Browse Amazing Photography | PhotoShare',
        'og_description': 'Browse thousands of amazing photos from talented photographers worldwide.',
        'og_type': 'website',
        'twitter_title': 'Photo Gallery - Browse Amazing Photography | PhotoShare',
        'twitter_description': 'Browse thousands of amazing photos from talented photographers worldwide.',
        'schema_type': 'CollectionPage',
    }
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query,
        'sort_by': sort_by,
        **seo_context,
    }
    return render(request, 'userApp/photo_list.html', context)

def photo_detail(request, photo_id):
    """Display individual photo with comments and details"""
    photo = get_object_or_404(Photo, id=photo_id, is_public=True)
    
    # Increment view count
    photo.views += 1
    photo.save()
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.photo = photo
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('userApp:photo_detail', photo_id=photo.id)
    else:
        comment_form = CommentForm()
    
    # Get related photos
    related_photos = Photo.objects.filter(
        Q(category=photo.category) | Q(photographer=photo.photographer)
    ).exclude(id=photo.id).filter(is_public=True)[:6]
    
    # SEO context
    seo_context = {
        'meta_title': f'{photo.title} by {photo.photographer.username} | PhotoShare',
        'meta_description': photo.description[:160] if photo.description else f'Amazing photo titled "{photo.title}" by {photo.photographer.username}. View and discover more photography on PhotoShare.',
        'meta_keywords': f'{photo.title}, {photo.photographer.username}, photography, photo, {photo.category.name if photo.category else ""}, {photo.tags}',
        'og_title': f'{photo.title} by {photo.photographer.username} | PhotoShare',
        'og_description': photo.description[:160] if photo.description else f'Amazing photo titled "{photo.title}" by {photo.photographer.username}.',
        'og_type': 'article',
        'og_image': request.build_absolute_uri(photo.image.url) if photo.image else '',
        'twitter_title': f'{photo.title} by {photo.photographer.username} | PhotoShare',
        'twitter_description': photo.description[:160] if photo.description else f'Amazing photo titled "{photo.title}" by {photo.photographer.username}.',
        'twitter_image': request.build_absolute_uri(photo.image.url) if photo.image else '',
        'schema_type': 'ImageObject',
    }
    
    context = {
        'photo': photo,
        'comment_form': comment_form,
        'related_photos': related_photos,
        **seo_context,
    }
    return render(request, 'userApp/photo_detail.html', context)

@login_required
def photo_upload(request):
    """Upload new photo"""
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.photographer = request.user
            photo.save()
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('userApp:photo_detail', photo_id=photo.id)
    else:
        form = PhotoUploadForm()
    
    # Calculate user statistics for the sidebar
    user_photos = request.user.photos.all()
    total_photos = user_photos.count()
    public_photos = user_photos.filter(is_public=True).count()
    total_views = sum(photo.views for photo in user_photos)
    
    # SEO context
    seo_context = {
        'meta_title': 'Upload Photo - Share Your Photography | PhotoShare',
        'meta_description': 'Upload and share your photography with the world. Join our community of photographers and showcase your creative vision.',
        'meta_keywords': 'upload photo, photo upload, share photography, photo sharing, photography community',
        'og_title': 'Upload Photo - Share Your Photography | PhotoShare',
        'og_description': 'Upload and share your photography with the world. Join our community of photographers.',
        'og_type': 'website',
        'twitter_title': 'Upload Photo - Share Your Photography | PhotoShare',
        'twitter_description': 'Upload and share your photography with the world. Join our community of photographers.',
        'schema_type': 'WebPage',
    }
    
    context = {
        'form': form,
        'total_photos': total_photos,
        'public_photos': public_photos,
        'total_views': total_views,
        **seo_context,
    }
    return render(request, 'userApp/photo_upload.html', context)

@login_required
def photo_edit(request, photo_id):
    """Edit existing photo"""
    photo = get_object_or_404(Photo, id=photo_id, photographer=request.user)
    
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photo updated successfully!')
            return redirect('userApp:photo_detail', photo_id=photo.id)
    else:
        form = PhotoUploadForm(instance=photo)
    
    # SEO context
    seo_context = {
        'meta_title': f'Edit Photo - {photo.title} | PhotoShare',
        'meta_description': f'Edit your photo "{photo.title}" on PhotoShare. Update details, tags, and settings.',
        'meta_keywords': 'edit photo, photo editing, update photo, photo management',
        'og_title': f'Edit Photo - {photo.title} | PhotoShare',
        'og_description': f'Edit your photo "{photo.title}" on PhotoShare.',
        'og_type': 'website',
        'twitter_title': f'Edit Photo - {photo.title} | PhotoShare',
        'twitter_description': f'Edit your photo "{photo.title}" on PhotoShare.',
        'schema_type': 'WebPage',
    }
    
    context = {
        'form': form,
        'photo': photo,
        **seo_context,
    }
    return render(request, 'userApp/photo_edit.html', context)

@login_required
def photo_delete(request, photo_id):
    """Delete photo"""
    photo = get_object_or_404(Photo, id=photo_id, photographer=request.user)
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Photo deleted successfully!')
        return redirect('userApp:user_photos', username=request.user.username)
    
    # SEO context
    seo_context = {
        'meta_title': f'Delete Photo - {photo.title} | PhotoShare',
        'meta_description': f'Confirm deletion of your photo "{photo.title}" on PhotoShare.',
        'meta_keywords': 'delete photo, photo deletion, remove photo',
        'og_title': f'Delete Photo - {photo.title} | PhotoShare',
        'og_description': f'Confirm deletion of your photo "{photo.title}" on PhotoShare.',
        'og_type': 'website',
        'twitter_title': f'Delete Photo - {photo.title} | PhotoShare',
        'twitter_description': f'Confirm deletion of your photo "{photo.title}" on PhotoShare.',
        'schema_type': 'WebPage',
    }
    
    context = {
        'photo': photo,
        **seo_context,
    }
    return render(request, 'userApp/photo_delete.html', context)

@require_POST
@login_required
def like_photo(request, photo_id):
    """Like/unlike a photo"""
    photo = get_object_or_404(Photo, id=photo_id)
    
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
        liked = False
    else:
        photo.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': photo.likes.count()
    })

def user_profile(request, username):
    """Display user profile with their photos"""
    user = get_object_or_404(CustomUser, username=username)
    photos = Photo.objects.filter(photographer=user, is_public=True).order_by('-created_at')
    
    # Check if current user is following this user
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    # Pagination for photos
    paginator = Paginator(photos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # SEO context
    seo_context = {
        'meta_title': f'{user.username} - Photographer Profile | PhotoShare',
        'meta_description': f'View {user.username}\'s photography portfolio on PhotoShare. Discover amazing photos and follow this talented photographer.',
        'meta_keywords': f'{user.username}, photographer, photography portfolio, photo gallery, {user.username} photos',
        'og_title': f'{user.username} - Photographer Profile | PhotoShare',
        'og_description': f'View {user.username}\'s photography portfolio on PhotoShare.',
        'og_type': 'profile',
        'og_image': request.build_absolute_uri(user.profile_image.url) if user.profile_image else '',
        'twitter_title': f'{user.username} - Photographer Profile | PhotoShare',
        'twitter_description': f'View {user.username}\'s photography portfolio on PhotoShare.',
        'twitter_image': request.build_absolute_uri(user.profile_image.url) if user.profile_image else '',
        'schema_type': 'Person',
    }
    
    context = {
        'profile_user': user,
        'page_obj': page_obj,
        'is_following': is_following,
        'followers_count': user.followers.count(),
        'following_count': user.following.count(),
        'photos_count': photos.count(),
        **seo_context,
    }
    return render(request, 'userApp/user_profile.html', context)

@login_required
def user_photos(request, username):
    """Display user's own photos (including private ones)"""
    if request.user.username != username:
        return redirect('userApp:user_profile', username=username)
    
    photos = Photo.objects.filter(photographer=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(photos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # SEO context
    seo_context = {
        'meta_title': f'My Photos - {request.user.username} | PhotoShare',
        'meta_description': f'Manage your photos on PhotoShare. View, edit, and organize your photography collection.',
        'meta_keywords': 'my photos, photo management, personal photo gallery, photo collection',
        'og_title': f'My Photos - {request.user.username} | PhotoShare',
        'og_description': f'Manage your photos on PhotoShare.',
        'og_type': 'website',
        'twitter_title': f'My Photos - {request.user.username} | PhotoShare',
        'twitter_description': f'Manage your photos on PhotoShare.',
        'schema_type': 'CollectionPage',
    }
    
    context = {
        'page_obj': page_obj,
        **seo_context,
    }
    return render(request, 'userApp/user_photos.html', context)

@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            # Check if user exists in database before redirecting
            try:
                # Verify the user exists in the database
                user_exists = CustomUser.objects.filter(username=request.user.username).exists()
                if user_exists:
                    return redirect('userApp:user_profile', username=request.user.username)
                else:
                    messages.error(request, 'User profile not found. Redirecting to home.')
                    return redirect('userApp:home')
            except Exception as e:
                messages.error(request, 'An error occurred. Redirecting to home.')
                return redirect('userApp:home')
    else:
        form = UserProfileForm(instance=request.user)
    
    # SEO context
    seo_context = {
        'meta_title': 'Edit Profile - PhotoShare',
        'meta_description': 'Update your profile information, bio, and profile picture on PhotoShare.',
        'meta_keywords': 'edit profile, profile settings, update profile, user settings',
        'og_title': 'Edit Profile - PhotoShare',
        'og_description': 'Update your profile information on PhotoShare.',
        'og_type': 'website',
        'twitter_title': 'Edit Profile - PhotoShare',
        'twitter_description': 'Update your profile information on PhotoShare.',
        'schema_type': 'WebPage',
    }
    
    context = {
        'form': form,
        **seo_context,
    }
    return render(request, 'userApp/profile_edit.html', context)

@require_POST
@login_required
def follow_user(request, username):
    """Follow/unfollow a user"""
    user_to_follow = get_object_or_404(CustomUser, username=username)
    
    if request.user == user_to_follow:
        return JsonResponse({'error': 'You cannot follow yourself'}, status=400)
    
    follow_obj, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    if not created:
        follow_obj.delete()
        is_following = False
    else:
        is_following = True
    
    return JsonResponse({
        'is_following': is_following,
        'followers_count': user_to_follow.followers.count()
    })

def album_list(request):
    """Display all public albums"""
    albums = Album.objects.filter(is_public=True)
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        albums = albums.order_by('created_at')
    elif sort_by == 'popular':
        albums = albums.annotate(photo_count=Count('photos')).order_by('-photo_count', '-created_at')
    elif sort_by == 'photos':
        albums = albums.annotate(photo_count=Count('photos')).order_by('-photo_count', '-created_at')
    else:  # newest
        albums = albums.order_by('-created_at')
    
    # Get statistics for the hero section
    total_albums = Album.objects.filter(is_public=True).count()
    total_photos = Photo.objects.filter(is_public=True).count()
    photographers_count = CustomUser.objects.filter(photos__is_public=True).distinct().count()
    
    # Pagination
    paginator = Paginator(albums, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # SEO context
    seo_context = {
        'meta_title': 'Photo Albums - Browse Photography Collections | PhotoShare',
        'meta_description': 'Discover amazing photo albums and photography collections from talented photographers worldwide.',
        'meta_keywords': 'photo albums, photography collections, photo collections, photo galleries, photography albums',
        'og_title': 'Photo Albums - Browse Photography Collections | PhotoShare',
        'og_description': 'Discover amazing photo albums and photography collections from talented photographers worldwide.',
        'og_type': 'website',
        'twitter_title': 'Photo Albums - Browse Photography Collections | PhotoShare',
        'twitter_description': 'Discover amazing photo albums and photography collections from talented photographers worldwide.',
        'schema_type': 'CollectionPage',
    }
    
    context = {
        'page_obj': page_obj,
        'total_albums': total_albums,
        'total_photos': total_photos,
        'photographers_count': photographers_count,
        'sort_by': sort_by,
        **seo_context,
    }
    return render(request, 'userApp/album_list.html', context)

def album_detail(request, album_id):
    """Display album with its photos"""
    album = get_object_or_404(Album, id=album_id, is_public=True)
    photos = album.photos.filter(is_public=True)
    
    # SEO context
    seo_context = {
        'meta_title': f'{album.title} - Photo Album by {album.photographer.username} | PhotoShare',
        'meta_description': f'View "{album.title}" photo album by {album.photographer.username}. {album.description[:120] if album.description else "Discover amazing photography in this collection."}',
        'meta_keywords': f'{album.title}, photo album, {album.photographer.username}, photography collection, photo gallery',
        'og_title': f'{album.title} - Photo Album by {album.photographer.username} | PhotoShare',
        'og_description': f'View "{album.title}" photo album by {album.photographer.username}.',
        'og_type': 'website',
        'og_image': request.build_absolute_uri(album.cover_photo.image.url) if album.cover_photo and album.cover_photo.image else '',
        'twitter_title': f'{album.title} - Photo Album by {album.photographer.username} | PhotoShare',
        'twitter_description': f'View "{album.title}" photo album by {album.photographer.username}.',
        'twitter_image': request.build_absolute_uri(album.cover_photo.image.url) if album.cover_photo and album.cover_photo.image else '',
        'schema_type': 'ImageGallery',
    }
    
    context = {
        'album': album,
        'photos': photos,
        **seo_context,
    }
    return render(request, 'userApp/album_detail.html', context)

@login_required
def album_create(request):
    """Create new album"""
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.photographer = request.user
            album.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Album created successfully!')
            return redirect('userApp:album_detail', album_id=album.id)
    else:
        form = AlbumForm()
    
    # SEO context
    seo_context = {
        'meta_title': 'Create Photo Album - PhotoShare',
        'meta_description': 'Create a new photo album to organize and showcase your photography collection.',
        'meta_keywords': 'create album, photo album, new album, photography collection',
        'og_title': 'Create Photo Album - PhotoShare',
        'og_description': 'Create a new photo album to organize and showcase your photography collection.',
        'og_type': 'website',
        'twitter_title': 'Create Photo Album - PhotoShare',
        'twitter_description': 'Create a new photo album to organize and showcase your photography collection.',
        'schema_type': 'WebPage',
    }
    
    context = {
        'form': form,
        **seo_context,
    }
    return render(request, 'userApp/album_create.html', context)

def category_photos(request, category_id):
    """Display photos by category"""
    category = get_object_or_404(Category, id=category_id)
    photos = Photo.objects.filter(category=category, is_public=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(photos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # SEO context
    seo_context = {
        'meta_title': f'{category.name} Photography - Browse {category.name} Photos | PhotoShare',
        'meta_description': f'Browse amazing {category.name} photography on PhotoShare. Discover stunning photos in the {category.name} category.',
        'meta_keywords': f'{category.name}, {category.name} photography, {category.name} photos, photography category',
        'og_title': f'{category.name} Photography - Browse {category.name} Photos | PhotoShare',
        'og_description': f'Browse amazing {category.name} photography on PhotoShare.',
        'og_type': 'website',
        'twitter_title': f'{category.name} Photography - Browse {category.name} Photos | PhotoShare',
        'twitter_description': f'Browse amazing {category.name} photography on PhotoShare.',
        'schema_type': 'CollectionPage',
    }
    
    context = {
        'category': category,
        'page_obj': page_obj,
        **seo_context,
    }
    return render(request, 'userApp/category_photos.html', context)

def search_results(request):
    """Search functionality"""
    query = request.GET.get('q', '')
    if query:
        photos = Photo.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query) |
            Q(photographer__username__icontains=query) |
            Q(location__icontains=query)
        ).filter(is_public=True).order_by('-created_at')
        
        # Pagination
        paginator = Paginator(photos, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None
    
    # SEO context
    seo_context = {
        'meta_title': f'Search Results for "{query}" - PhotoShare' if query else 'Search Photos - PhotoShare',
        'meta_description': f'Search results for "{query}" on PhotoShare. Find amazing photography and photographers.' if query else 'Search for amazing photography and photographers on PhotoShare.',
        'meta_keywords': f'search photos, {query}, photography search, find photos, photo search',
        'og_title': f'Search Results for "{query}" - PhotoShare' if query else 'Search Photos - PhotoShare',
        'og_description': f'Search results for "{query}" on PhotoShare.' if query else 'Search for amazing photography on PhotoShare.',
        'og_type': 'website',
        'twitter_title': f'Search Results for "{query}" - PhotoShare' if query else 'Search Photos - PhotoShare',
        'twitter_description': f'Search results for "{query}" on PhotoShare.' if query else 'Search for amazing photography on PhotoShare.',
        'schema_type': 'SearchResultsPage',
    }
    
    context = {
        'query': query,
        'page_obj': page_obj,
        **seo_context,
    }
    return render(request, 'userApp/search_results.html', context)

# Authentication Views
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('userApp:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            login(request, user)
            messages.success(request, f'Welcome to PhotoShare, {user.username}! Your account has been created successfully.')
            return redirect('userApp:home')
    else:
        form = CustomUserCreationForm()
    
    # SEO context
    seo_context = {
        'meta_title': 'Sign Up - Join PhotoShare Photography Community',
        'meta_description': 'Join PhotoShare and start sharing your photography with the world. Create your free account today.',
        'meta_keywords': 'sign up, register, join, photography community, photo sharing, free account',
        'og_title': 'Sign Up - Join PhotoShare Photography Community',
        'og_description': 'Join PhotoShare and start sharing your photography with the world.',
        'og_type': 'website',
        'twitter_title': 'Sign Up - Join PhotoShare Photography Community',
        'twitter_description': 'Join PhotoShare and start sharing your photography with the world.',
        'schema_type': 'WebPage',
    }
    
    context = {
        'form': form,
        **seo_context,
    }
    return render(request, 'userApp/register.html', context)

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('userApp:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect to next page if specified, otherwise to home
                next_page = request.GET.get('next')
                if next_page and next_page != '/':
                    return redirect(next_page)
                else:
                    return redirect('userApp:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()
    
    # SEO context
    seo_context = {
        'meta_title': 'Login - PhotoShare Photography Community',
        'meta_description': 'Login to your PhotoShare account and continue sharing your photography with the world.',
        'meta_keywords': 'login, sign in, photography community, photo sharing, user account',
        'og_title': 'Login - PhotoShare Photography Community',
        'og_description': 'Login to your PhotoShare account and continue sharing your photography.',
        'og_type': 'website',
        'twitter_title': 'Login - PhotoShare Photography Community',
        'twitter_description': 'Login to your PhotoShare account and continue sharing your photography.',
        'schema_type': 'WebPage',
    }
    
    context = {
        'form': form,
        **seo_context,
    }
    return render(request, 'userApp/login.html', context)

def logout_view(request):
    """User logout view"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
    return redirect('userApp:home')

def password_reset_view(request):
    """Simple password reset view"""
    if request.user.is_authenticated:
        return redirect('userApp:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # In a real application, you would send an email here
            # For now, we'll just show a success message
            messages.success(request, f'If an account with email {email} exists, you will receive a password reset link shortly.')
            return redirect('userApp:login')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    # Create a simple form for email input
    from django import forms
    class PasswordResetForm(forms.Form):
        email = forms.EmailField()
    
    form = PasswordResetForm()
    
    # SEO context
    seo_context = {
        'meta_title': 'Reset Password - PhotoShare',
        'meta_description': 'Reset your PhotoShare password. Enter your email address to receive a password reset link.',
        'meta_keywords': 'reset password, forgot password, password recovery, account recovery',
        'og_title': 'Reset Password - PhotoShare',
        'og_description': 'Reset your PhotoShare password. Enter your email address to receive a password reset link.',
        'og_type': 'website',
        'twitter_title': 'Reset Password - PhotoShare',
        'twitter_description': 'Reset your PhotoShare password. Enter your email address to receive a password reset link.',
        'schema_type': 'WebPage',
    }
    
    context = {
        'form': form,
        **seo_context,
    }
    return render(request, 'userApp/password_reset.html', context)

def sitemap(request):
    """Display site map with all navigation options"""
    # Get some statistics for the sitemap
    total_photos = Photo.objects.filter(is_public=True).count()
    total_users = CustomUser.objects.count()
    total_albums = Album.objects.filter(is_public=True).count()
    total_categories = Category.objects.count()
    
    # SEO context
    seo_context = {
        'meta_title': 'Sitemap - PhotoShare',
        'meta_description': 'Complete sitemap of PhotoShare. Find all pages, photos, albums, and photographers on our photography platform.',
        'meta_keywords': 'sitemap, site map, photo gallery, photography platform, navigation',
        'og_title': 'Sitemap - PhotoShare',
        'og_description': 'Complete sitemap of PhotoShare. Find all pages and content on our photography platform.',
        'og_type': 'website',
        'twitter_title': 'Sitemap - PhotoShare',
        'twitter_description': 'Complete sitemap of PhotoShare. Find all pages and content on our photography platform.',
        'schema_type': 'WebPage',
    }
    
    context = {
        'total_photos': total_photos,
        'total_users': total_users,
        'total_albums': total_albums,
        'total_categories': total_categories,
        **seo_context,
    }
    return render(request, 'userApp/sitemap.html', context)

def sitemap_xml(request):
    """Generate XML sitemap for search engines"""
    # Get all public photos, albums, categories, and users
    photos = Photo.objects.filter(is_public=True).order_by('-created_at')
    albums = Album.objects.filter(is_public=True).order_by('-created_at')
    categories = Category.objects.all()
    users = CustomUser.objects.filter(photos__is_public=True).distinct()
    
    # Base URL
    base_url = request.build_absolute_uri('/')[:-1]  # Remove trailing slash
    
    # Generate sitemap XML
    xml_content = render_to_string('userApp/sitemap.xml', {
        'base_url': base_url,
        'photos': photos,
        'albums': albums,
        'categories': categories,
        'users': users,
        'lastmod': timezone.now().strftime('%Y-%m-%d'),
    })
    
    return HttpResponse(xml_content, content_type='application/xml')

def robots_txt(request):
    """Generate robots.txt file"""
    robots_content = """User-agent: *
Allow: /

# Sitemap
Sitemap: {}/sitemap.xml

# Disallow admin and private areas
Disallow: /admin/
Disallow: /private/
Disallow: /accounts/
""".format(request.build_absolute_uri('/')[:-1])
    
    return HttpResponse(robots_content, content_type='text/plain')
