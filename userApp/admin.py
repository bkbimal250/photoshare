from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Photo, Album, Category, Comment, Follow

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('profile_image', 'bio', 'website', 'location')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile Info', {'fields': ('profile_image', 'bio', 'website', 'location')}),
    )

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'photographer', 'category', 'views', 'likes_count', 'is_public', 'created_at')
    list_filter = ('is_public', 'category', 'created_at', 'photographer')
    search_fields = ('title', 'description', 'photographer__username', 'tags')
    readonly_fields = ('views', 'created_at', 'updated_at')
    list_editable = ('is_public',)
    
    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'photographer', 'photo_count', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at', 'photographer')
    search_fields = ('title', 'description', 'photographer__username')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_public',)
    
    def photo_count(self, obj):
        return obj.get_photo_count()
    photo_count.short_description = 'Photos'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_count', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Photos'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'content_preview', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username', 'photo__title')
    readonly_fields = ('created_at', 'updated_at')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    readonly_fields = ('created_at',)

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
