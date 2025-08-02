#!/usr/bin/env python
"""
Script to create a demo user for testing the PhotoShare application.
Run this script from the Django project directory.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photography.settings')
django.setup()

from userApp.models import CustomUser, Category

def create_demo_user():
    """Create a demo user for testing"""
    try:
        # Check if demo user already exists
        demo_user, created = CustomUser.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'bio': 'This is a demo account for testing the PhotoShare application.',
                'website': 'https://example.com',
                'location': 'Demo City, Demo Country',
            }
        )
        
        if created:
            # Set password
            demo_user.set_password('demo123456')
            demo_user.save()
            print("✅ Demo user created successfully!")
            print(f"   Username: demo")
            print(f"   Password: demo123456")
            print(f"   Email: demo@example.com")
        else:
            # Update password if user exists
            demo_user.set_password('demo123456')
            demo_user.save()
            print("✅ Demo user password updated!")
            print(f"   Username: demo")
            print(f"   Password: demo123456")
            print(f"   Email: demo@example.com")
        
        return demo_user
        
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        return None

def create_sample_categories():
    """Create sample categories for the application"""
    categories = [
        'Landscape',
        'Portrait',
        'Street',
        'Nature',
        'Architecture',
        'Wildlife',
        'Macro',
        'Black & White',
        'Abstract',
        'Travel',
        'Food',
        'Fashion',
    ]
    
    created_count = 0
    for category_name in categories:
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={
                'description': f'Photos in the {category_name.lower()} category'
            }
        )
        if created:
            created_count += 1
    
    print(f"✅ Created {created_count} new categories!")
    print(f"   Total categories: {Category.objects.count()}")

def main():
    """Main function to set up demo data"""
    print("🚀 Setting up demo data for PhotoShare...")
    print()
    
    # Create demo user
    demo_user = create_demo_user()
    print()
    
    # Create sample categories
    create_sample_categories()
    print()
    
    print("🎉 Demo setup complete!")
    print()
    print("You can now:")
    print("1. Run the development server: python manage.py runserver")
    print("2. Visit http://localhost:8000")
    print("3. Login with the demo account:")
    print("   - Username: demo")
    print("   - Password: demo123456")
    print()
    print("Or register a new account at http://localhost:8000/register/")

if __name__ == '__main__':
    main() 