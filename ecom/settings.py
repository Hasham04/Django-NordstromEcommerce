import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "12345"
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',

    'cart',
    'core',
    'staff'
]

DEFAULT_FROM_EMAIL = 'hasham610@gmail.com'
NOTIFY_EMAIL = 'hasham610@gmail.com'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_REDIRECT_URL = '/'
SITE_ID = 1
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

PAYPAL_CLIENT_ID = 'AX2YkGhYI41w6JowDxpqVcaKyzl90ZQxUF5zqw02ruhohKDz9c_SPsy7v-A5t_S3oTG5Y2DM2meqcSmR'
PAYPAL_SECRET_KEY = 'EIZPdT1ZtI7xjuo7r8qCBGSi2EdqmmLr6_qGaSFjxcCgIlO9SrJsMn6mtyshTguj0zhd-deHNKzV4VzD'

if DEBUG is False:
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    ALLOWED_HOSTS = ['www.domain.com']
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': ''
        }
    }

    PAYPAL_CLIENT_ID = 'AWgNHknwQAXsQFGznVfNuM5TiS0SHHG6aeSP1CZ0ns5RSmbEVcoM54EulE2U2RaOEtC21vZsE_vGuiT6'
    PAYPAL_SECRET_KEY = 'EFY5KUmxbOCls5xqQkrRnFyk8jhw6Z3NPVtMPkWmgHDwBx_Cqib4u-eQ_7pgC-UWab28K22mVX3fFOUB'
