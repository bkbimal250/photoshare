# 🚀 PhotoShare Quick Start Guide

Get PhotoShare up and running in 5 minutes!

## Prerequisites

- **Python 3.11+**
- **Node.js 16+**
- **Git**

## Option 1: Automated Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd photography

# Run the automated installer
python install.py
```

The installer will:
- ✅ Check Python and Node.js versions
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Set up Tailwind CSS
- ✅ Configure database
- ✅ Collect static files
- ✅ Guide you through superuser creation

## Option 2: Manual Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd photography
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
cd theme/static_src
npm install
npm run build
cd ../..
```

### 3. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Run the Server
```bash
python manage.py runserver
```

## 🎯 You're Ready!

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 📱 First Steps

1. **Visit the website** and explore the interface
2. **Create an account** or use the admin panel
3. **Upload your first photo** using the upload feature
4. **Explore categories** and other users' photos
5. **Customize your profile** with bio and profile image

## 🛠️ Development

### Start Development Server
```bash
python manage.py runserver
```

### Tailwind CSS Auto-reload
```bash
cd theme/static_src
npm run dev
```

### Database Changes
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🆘 Common Issues

### "rimraf is not recognized"
```bash
cd theme/static_src
npm install
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Database errors
```bash
python manage.py migrate
```

### Python version issues
Make sure you're using Python 3.11 or higher:
```bash
python --version
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [STATIC_FILES_SETUP.md](STATIC_FILES_SETUP.md) for static files configuration
- Review [SEO_OPTIMIZATION.md](SEO_OPTIMIZATION.md) for SEO features

## 🎉 Welcome to PhotoShare!

You now have a fully functional photography community platform running locally. Start sharing your photos and connecting with other photographers!

---

**Need help?** Check the main [README.md](README.md) or open an issue on GitHub. 