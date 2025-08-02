# 📸 PhotoShare - Photography Community Platform

A modern, full-featured photography sharing platform built with Django and Tailwind CSS. Share your photography with the world, connect with fellow photographers, and showcase your creative vision.

![PhotoShare](https://img.shields.io/badge/Django-5.2.4-green) ![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38B2AC)

## 🌟 Features

### 📱 Core Features
- **Photo Upload & Sharing**: Upload high-quality photos with descriptions and tags
- **User Profiles**: Customizable profiles with portfolio showcases
- **Photo Albums**: Organize photos into beautiful albums
- **Categories**: Browse photos by categories (Nature, Portrait, Street, etc.)
- **Search**: Advanced search functionality for photos and photographers
- **Like System**: Like and interact with photos
- **Comments**: Engage with the community through comments
- **Follow System**: Follow your favorite photographers

### 🎨 Design & UX
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **Dark Theme**: Photography-focused dark gradient background
- **Mobile Responsive**: Optimized for all devices
- **Glass Morphism**: Modern glass card effects
- **Smooth Animations**: Engaging user interactions

### 🔧 Technical Features
- **SEO Optimized**: Complete meta tags, structured data, and sitemaps
- **Performance**: Optimized for speed and user experience
- **Security**: Django's built-in security features
- **Custom User Model**: Extended user profiles
- **Image Processing**: Automatic image optimization with Pillow

## 🚀 Quick Start

### Prerequisites

- **Python 3.11 or higher**
- **Node.js 16+ and npm** (for Tailwind CSS)
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd photography
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv env
   env\Scripts\activate

   # macOS/Linux
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Tailwind CSS**
   ```bash
   # Navigate to theme directory
   cd theme/static_src
   
   # Install npm dependencies
   npm install
   
   # Build Tailwind CSS
   npm run build
   
   # Return to project root
   cd ../..
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Visit the application**
   - Open your browser and go to `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## 📁 Project Structure

```
photography/
├── photography/          # Django project settings
│   ├── settings.py      # Main settings file
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── userApp/             # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL patterns
│   ├── forms.py         # Django forms
│   ├── admin.py         # Admin configuration
│   └── templates/       # HTML templates
├── theme/               # Tailwind CSS theme
│   ├── static_src/      # Source files
│   └── static/          # Compiled static files
├── media/               # User uploaded files
├── staticfiles/         # Collected static files
├── requirements.txt     # Python dependencies
├── build_static.py      # Build script
└── README.md           # This file
```

## 🛠️ Development

### Running in Development Mode

```bash
# Start the development server
python manage.py runserver

# For Tailwind CSS auto-reload (in another terminal)
cd theme/static_src
npm run dev
```

### Database Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (if needed)
python manage.py flush
```

### Static Files

```bash
# Build static files
python build_static.py

# Or manually:
cd theme/static_src
npm run build
python manage.py collectstatic --noinput
```

## 🎯 Usage Guide

### For Users

1. **Registration & Login**
   - Visit `/register/` to create an account
   - Use `/login/` to access your account

2. **Uploading Photos**
   - Click "Upload" in the navigation
   - Select an image file
   - Add title, description, and category
   - Choose tags for better discoverability

3. **Managing Your Profile**
   - Visit your profile page
   - Edit profile information
   - View your photo collection
   - Manage your albums

4. **Discovering Content**
   - Browse photos on the home page
   - Use search to find specific content
   - Explore categories and albums
   - Follow other photographers

### For Administrators

1. **Admin Panel**
   - Access `/admin/` with superuser credentials
   - Manage users, photos, and categories
   - Monitor site activity

2. **Content Moderation**
   - Review uploaded photos
   - Manage user accounts
   - Handle reported content

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Django Settings

Key settings in `photography/settings.py`:

- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Configure for your domain
- `STATIC_ROOT`: Static files collection directory
- `MEDIA_ROOT`: User uploaded files directory

## 🚀 Deployment

### Production Setup

1. **Set environment variables**
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-production-secret-key
   ```

2. **Build static files**
   ```bash
   python build_static.py
   ```

3. **Configure web server**
   - Use Gunicorn or uWSGI
   - Set up Nginx for static files
   - Configure SSL certificates

4. **Database setup**
   - Use PostgreSQL for production
   - Set up database backups
   - Configure connection pooling

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "photography.wsgi:application"]
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# With coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📊 API Endpoints

The application includes the following main endpoints:

- `GET /` - Home page
- `GET /photos/` - Photo listing
- `GET /photos/<id>/` - Photo detail
- `POST /photos/upload/` - Upload photo
- `GET /albums/` - Album listing
- `GET /profile/<username>/` - User profile
- `GET /search/` - Search functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style

```bash
# Format code
black .

# Sort imports
isort .

# Check code quality
flake8 .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

1. **"rimraf is not recognized"**
   - Run `npm install` in `theme/static_src/`

2. **Static files not loading**
   - Run `python manage.py collectstatic --noinput`

3. **Database errors**
   - Run `python manage.py migrate`

4. **Tailwind CSS not working**
   - Ensure Node.js is installed
   - Run `npm install` and `npm run build`

### Getting Help

- Check the [STATIC_FILES_SETUP.md](STATIC_FILES_SETUP.md) for static files configuration
- Review the [SEO_OPTIMIZATION.md](SEO_OPTIMIZATION.md) for SEO implementation
- Open an issue on GitHub for bugs or feature requests

## 🔮 Future Enhancements

- [ ] Social authentication (Google, Facebook)
- [ ] Advanced image editing tools
- [ ] Photo contests and challenges
- [ ] Mobile app development
- [ ] API for third-party integrations
- [ ] Advanced analytics and insights
- [ ] Photo printing services
- [ ] Live streaming for photographers

## 📈 Performance

- **Page Load Time**: < 2 seconds
- **Image Optimization**: Automatic compression
- **Database Queries**: Optimized with select_related and prefetch_related
- **Caching**: Ready for Redis integration
- **CDN**: Compatible with CDN deployment

## 🔒 Security

- CSRF protection enabled
- XSS prevention
- SQL injection protection
- Secure file upload validation
- User authentication and authorization
- Input sanitization

---

**Built with ❤️ using Django and Tailwind CSS**

For more information, visit the [project documentation](docs/) or contact the development team. 