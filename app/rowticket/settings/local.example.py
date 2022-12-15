DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rowticket',
        'USER': 'rowticket',
        'PASSWORD': 'rowticket',
        'HOST': 'localhost',
        'PORT': ''
    }
}

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000'
]
