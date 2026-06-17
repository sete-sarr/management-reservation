from .base import *
DEBUG = False
ADMINS = [
('Antonio M', 'admin@gmail.com'),
]
ALLOWED_HOSTS = ['*']
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
 'NAME': BASE_DIR / 'db.sqlite3',
}
}