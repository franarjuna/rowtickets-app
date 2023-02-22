ALLOWED_HOSTS = []

SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd70l7ecjc521qp',
        'USER': 'cozanhbicwukpx',
        'PASSWORD': 'e1fb4734b5527d218170d292e936fcffad2dd2a1e2a782708fdf31468274300c',
        'HOST': 'ec2-34-194-73-236.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000'
]
