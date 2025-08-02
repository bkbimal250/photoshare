#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photography.settings')
django.setup()

from userApp.models import CustomUser, Photo, Album, Category
from django.db.models import Count

def check_database():
    """Check the current state of the database"""
    print("=== Database Status Check ===")
    
    # Check users
    users_count = CustomUser.objects.count()
    print(f"Total Users: {users_count}")
    
    # Check categories
    categories_count = Category.objects.count()
    print(f"Total Categories: {categories_count}")
    
    # Check photos
    photos_count = Photo.objects.count()
    public_photos_count = Photo.objects.filter(is_public=True).count()
    print(f"Total Photos: {photos_count}")
    print(f"Public Photos: {public_photos_count}")
    
    # Check albums
    albums_count = Album.objects.count()
    public_albums_count = Album.objects.filter(is_public=True).count()
    print(f"Total Albums: {albums_count}")
    print(f"Public Albums: {public_albums_count}")
    
    # Check photographers (users with photos)
    photographers_count = CustomUser.objects.filter(photos__is_public=True).distinct().count()
    print(f"Photographers with public photos: {photographers_count}")
    
    print("\n=== Sample Data ===")
    
    # Create sample data if database is empty
    if users_count == 0:
        print("Creating sample user...")
        user = CustomUser.objects.create_user(
            username='demo',
            email='demo@example.com',
            password='demo123456',
            first_name='Demo',
            last_name='User'
        )
        print(f"Created user: {user.username}")
    
    if categories_count == 0:
        print("Creating sample categories...")
        categories = [
            'Nature', 'Portrait', 'Landscape', 'Street', 'Architecture', 'Wildlife'
        ]
        for cat_name in categories:
            category = Category.objects.create(name=cat_name)
            print(f"Created category: {category.name}")
    
    # Show final counts
    print("\n=== Final Database Status ===")
    print(f"Total Users: {CustomUser.objects.count()}")
    print(f"Total Categories: {Category.objects.count()}")
    print(f"Total Photos: {Photo.objects.count()}")
    print(f"Total Albums: {Album.objects.count()}")
    print(f"Photographers: {CustomUser.objects.filter(photos__is_public=True).distinct().count()}")

if __name__ == '__main__':
    check_database() 