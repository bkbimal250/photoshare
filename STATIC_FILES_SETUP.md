# Static Files Setup Guide

## Overview
This guide explains how to set up static files for the photography project and resolve common build issues.

## Current Configuration

### Django Settings
- `STATIC_URL = 'static/'` - URL prefix for static files
- `STATIC_ROOT = BASE_DIR / 'staticfiles'` - Directory for collected static files
- `STATICFILES_DIRS = [BASE_DIR / 'theme' / 'static', BASE_DIR / 'userApp' / 'static']` - Additional static file directories

### Directory Structure
```
photography/
├── theme/
│   ├── static_src/          # Source files for Tailwind CSS
│   │   ├── src/styles.css   # Main CSS input file
│   │   ├── package.json     # npm dependencies
│   │   └── tailwind.config.js
│   └── static/              # Compiled static files
│       └── css/dist/styles.css
├── userApp/
│   └── static/              # App-specific static files
└── staticfiles/             # Collected static files (generated)
```

## Quick Setup

### Option 1: Use the Build Script (Recommended)
```bash
python build_static.py
```

This script will:
1. Install npm dependencies
2. Build Tailwind CSS
3. Collect Django static files

### Option 2: Manual Setup

#### Step 1: Install npm dependencies
```bash
cd theme/static_src
npm install
```

#### Step 2: Build Tailwind CSS
```bash
npm run build
```

#### Step 3: Collect Django static files
```bash
python manage.py collectstatic --noinput
```

## Development vs Production

### Development Mode (DEBUG=True)
- Uses Tailwind CSS CDN for faster development
- No build step required
- Changes reflect immediately

### Production Mode (DEBUG=False)
- Uses compiled CSS from `theme/static/css/dist/styles.css`
- Requires build step before deployment
- Better performance and smaller file sizes

## Common Issues and Solutions

### 1. "rimraf is not recognized"
**Cause**: npm dependencies not installed
**Solution**: Run `npm install` in `theme/static_src/`

### 2. "STATICFILES_DIRS directory does not exist"
**Cause**: Static directories not created
**Solution**: The build script creates these automatically

### 3. "cdn.tailwindcss.com should not be used in production"
**Cause**: Using CDN in production
**Solution**: Set `DEBUG=False` and build static files

### 4. Missing autocomplete attributes
**Solution**: Already fixed in templates

### 5. Deprecated meta tags
**Solution**: Already updated in base.html

## Development Workflow

### For CSS changes:
1. Edit `theme/static_src/src/styles.css`
2. Run `npm run dev` in `theme/static_src/` for auto-reload
3. Or run `npm run build` for one-time build

### For new static files:
1. Add files to `theme/static/` or `userApp/static/`
2. Run `python manage.py collectstatic --noinput`

## File Locations

### CSS Files
- **Source**: `theme/static_src/src/styles.css`
- **Compiled**: `theme/static/css/dist/styles.css`
- **Collected**: `staticfiles/css/dist/styles.css`

### JavaScript Files
- **Location**: `theme/static/js/` or `userApp/static/js/`
- **Usage**: `<script src="{% static 'js/filename.js' %}">`

### Images
- **Location**: `theme/static/images/` or `userApp/static/images/`
- **Usage**: `<img src="{% static 'images/filename.jpg' %}">`

## Performance Tips

1. **Use compiled CSS in production** for better performance
2. **Minify static files** using Django's compression
3. **Use CDN for external libraries** (Font Awesome, Google Fonts)
4. **Optimize images** before adding to static files
5. **Use browser caching** for static files

## Troubleshooting

### Build fails with npm errors
```bash
cd theme/static_src
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Static files not loading
1. Check `STATIC_URL` in settings
2. Ensure `collectstatic` was run
3. Verify file paths in templates
4. Check browser console for 404 errors

### CSS not updating
1. Clear browser cache
2. Rebuild static files
3. Check if using CDN vs compiled CSS
4. Verify file permissions

## Next Steps

1. Run the build script: `python build_static.py`
2. Test the application: `python manage.py runserver`
3. For development: `npm run dev` in `theme/static_src/`
4. For production: Set `DEBUG=False` and build static files 