from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Photo, Album, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'bio', 'website', 'location', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'category', 'tags', 'location', 'camera_settings', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={'placeholder': 'nature, landscape, sunset (comma-separated)'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
            'camera_settings': forms.TextInput(attrs={'placeholder': 'Camera, lens, settings'}),
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'cover_photo', 'photos', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'photos': forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment here...',
                'class': 'form-control'
            }),
        }
        labels = {
            'content': 'Comment'
        } 