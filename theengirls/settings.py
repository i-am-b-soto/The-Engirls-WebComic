"""

View App on: https://dashboard.heroku.com/apps/theengirls


Django settings for theengirls project.

"""

import os
import dj_database_url

########### Remove this before deploying to Heroku ###########
from set_environ import set_environ 
set_environ()

########## Heroku Specific Settings ##########################
def set_default_db(DATABASES):
    if os.environ.get('on_heroku') or os.environ.get('on_heroku') == 'True':
        prod_db  =  dj_database_url.config(conn_max_age=500)
        DATABASES['default'].update(prod_db)

def set_CSRF_COOKIE_SECURE():
    if os.environ.get('on_heroku'):
        return True
    else:
        return False

######## Base Directory ######################################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


###########################################
# Custom Values
###########################################

MAIN_SERIES_NAME = "main" # The name the website will look for to determine which comics are the main series

CONTENT_KEY_NAMES = {
    'LANDING_PAGE_CONTENT_NAME' : 'LANDING_PAGE_CONTENT' # The name of the 'content' the website will use to display the landing page
    
    ,'ERROR_404_CONTENT_NAME' : 'ERROR_404_CONTENT' # The name of the 'content' the website will use to display 404 errors 
    ,'ERROR_400_CONTENT_NAME' : 'ERROR_400_CONTENT' # The Name of the 'content' the website will use to display 400 errors
    ,'ERROR_500_CONTENT_NAME' : 'ERROR_500_CONTENT' # The Name of the 'content' the website will use to display 500 errors

    ,'EMAIL_THANKS_CONTENT_NAME' : 'EMAIL_THANKS_CONTENT' # The name of the 'content' the website will use when distributing thank you emails
    ,'EMAIL_NEWS_CONTENT_NAME' : 'EMAIL_NEWS_CONTENT' # The name of the 'content' the website will use when distributing news emails
    ,'EMAIL_UNSUBSCRIBE_NAME' : 'EMAIL_UNSUBSCRIBE' # The name of the 'content' the website will use when distributing unsubscrine emails
}


COMMENTS_PAGINATOR_COUNT = 8 # Number of comments per page
MAX_COMMENTS_PER_USER_PER_PAGE = 25 # Maximum number of comments a user can make per page
THUMBNAIL_SIZE = (330, 420) # Thumbnail size ** CAUTION WHEN CHANGING THIS ***
COMIC_PAGINATOR_COUNT = 8 # Number of comics to view per archive page
BLOG_POST_PAGINATION_COUNT = 5 # Number of blog posts per page



###########################################
# Gmail 
###########################################
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'theintrocode@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


############################################
# Enviornment variables
#############################################

#FB_VALUES 
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY', None) # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET', None)  # App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_KEY', None)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_SECRET', None)
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SECRET_KEY = os.environ.get('Django_App_Key', None) 

AWS_ACCESS_KEY_ID = os.environ.get('AMAZON_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY =  os.environ.get('AMAZON_ACCESS_SECRET')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3-us-west-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = 'us-west-1'

############################################
# login/logout values
#############################################


LOGOUT_URL = 'custom_logout'
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


############################################
# WSGI
#############################################

WSGI_APPLICATION = 'theengirls.wsgi.application'

############################################
# DEBUG settings
#############################################

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['theengirls.herokuapp.com', '192.168.1.6']
ALLOWED_HOSTS.append('localhost')
ALLOWED_HOSTS.append('localhost:8000')

############################################
# Installed Apps
#############################################

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'dal',
    'dal_select2',      
    'ckeditor',
    'ckeditor_uploader',
    'comics',
    'blog',
    'comments',
    'content',
    'subscriptions',
    'django_filters',
    'social_django',
    'django.contrib.admin',
    'django.contrib.auth', 
    'storages',
]

############################################
# Some Middleware...
#############################################

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware', #<-- Social Django
]

############################################
# Template processors
#############################################

ROOT_URLCONF = 'theengirls.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # <-- Social Django
                'social_django.context_processors.login_redirect', # <-- Social Django
            ],
        },
    },
]


############################################
# Social Auth
#############################################

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    #'django.contrib.auth.backends.ModelBackend', <-- Default user authentication
    'theengirls.auth_backend.CaseInsensitiveModelBackend', # < -- Case insensetive Authentication 

)


############################################
# Database
#############################################
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

set_default_db(DATABASES)

############################################
# CSRF cookie secure
#############################################
CSRF_COOKIE_SECURE = set_CSRF_COOKIE_SECURE()


############################################
# Password Validation
#############################################
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

############################################
# Internationalization
#############################################

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



####################################
    ##  CKEDITOR CONFIGURATION ##
####################################
 
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
 
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
 
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}
 

############################################
# STATIC CONFIGURATION - Must be changed when 
# deploying to different servers
#############################################



STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


STATICFILES_DIRS = (
    # This is where static files for the whole site will be stored
    os.path.join(BASE_DIR, 'theengirls/static/'),
)


STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'theengirls.storage_backends.MediaStorage' 