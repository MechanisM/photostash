import os
import dj_database_url


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


DEBUG = os.environ.get('DEBUG', 'false') == 'true'
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = os.environ.get('SECRET_KEY', 'YOUR ENV SHOULD SET THIS')
SITE_ID = 1
ROOT_URLCONF = 'photostash.urls'
WSGI_APPLICATION = 'photostash.wsgi.application'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True


DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///%s' % os.path.join(PROJECT_ROOT, 'photostash.db')
    ),
}


MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads')
MEDIA_URL = '/uploads/'
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'uploads.photostash.com'


TEMPLATE_DIRS = ()
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)


INSTALLED_APPS = (
    'tastypie',
    'photostash.photos',
)


TEST_DISCOVERY_ROOT = os.path.join(PROJECT_ROOT, 'tests')
TEST_RUNNER = 'discover_runner.DiscoverRunner'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
