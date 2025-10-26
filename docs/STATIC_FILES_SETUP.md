# Static Files Setup Guide

## Overview
This document outlines the static files configuration for the Django migration of Appointment360.

## Static Files Structure

```
static/
├── css/
│   ├── sb-admin-2.min.css
│   └── sb-admin-2.css
├── js/
│   └── sb-admin-2.min.js
├── img/
│   └── undraw_profile.svg
├── vendor/
│   ├── bootstrap/
│   │   └── js/
│   │       └── bootstrap.bundle.min.js
│   ├── fontawesome-free/
│   │   ├── css/
│   │   │   └── all.min.css
│   │   └── webfonts/
│   ├── datatables/
│   │   ├── dataTables.bootstrap4.min.css
│   │   └── dataTables.bootstrap4.min.js
│   ├── jquery/
│   │   └── jquery.min.js
│   └── jquery-easing/
│       └── jquery.easing.min.js
```

## Copying Instructions

### Option 1: Use CDN (Recommended for Development)
The templates are already configured to use CDN for most libraries:
- jQuery: https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js
- Bootstrap: Included via CDN
- Font Awesome: Included via CDN
- DataTables: Included via CDN
- Select2: Included via CDN

### Option 2: Copy Static Files Manually
Copy the following files from `Laravel/assets/` to `static/`:

```bash
# Copy CSS
copy Laravel\assets\css\sb-admin-2.min.css static\css\
copy Laravel\assets\css\sb-admin-2.css static\css\

# Copy JS
copy Laravel\assets\js\sb-admin-2.min.js static\js\
copy Laravel\assets\js\jquery.dataTables.min.js static\js\

# Copy Images
copy Laravel\assets\img\*.svg static\img\

# Copy Vendor Files
copy Laravel\assets\vendor\bootstrap\js\bootstrap.bundle.min.js static\vendor\bootstrap\js\
copy Laravel\assets\vendor\jquery\jquery.min.js static\vendor\jquery\
copy Laravel\assets\vendor\jquery-easing\jquery.easing.min.js static\vendor\jquery-easing\
copy Laravel\assets\vendor\fontawesome-free\css\all.min.css static\vendor\fontawesome-free\css\
copy Laravel\assets\vendor\fontawesome-free\webfonts\* static\vendor\fontawesome-free\webfonts\
copy Laravel\assets\vendor\datatables\*.min.css static\vendor\datatables\
copy Laravel\assets\vendor\datatables\*.min.js static\vendor\datatables\
```

## Django Settings Configuration

Already configured in `settings.py`:
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# During development
if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
```

## Collection Command

Run after copying files:
```bash
python manage.py collectstatic --noinput
```

## CDN References in Templates

Templates use CDN for faster loading. To use local files instead, update template references from:
- `{% static 'vendor/jquery/jquery.min.js' %}`
to local paths or update static file collections.

## Current Status

✅ Templates configured to use CDN
✅ Settings configured for static files
⏳ Static files need to be copied from Laravel project
⏳ Collectstatic needs to be run

