"""

View App on: https://dashboard.heroku.com/apps/theengirls




Django settings for theengirls project.



Please reconfigure Social auth settings once deployed

for Google: https://console.developers.google.com/
Instructions on setting up Google: https://medium.com/trabe/oauth-authentication-in-django-with-social-auth-c67a002479c1
for Facebook: https://developers.facebook.com/

Logout redirect information:
https://rcpaul.wordpress.com/2011/08/28/logoutredirect/



"""

import os
import dj_database_url

########### Remove this before deploying to Heroku ###########
#from set_environ import set_environ 
#set_environ()
###################################################

def set_default_db(DATABASES):
    if os.environ.get('on_heroku') or os.environ.get('on_heroku') == 'True':
        prod_db  =  dj_database_url.config(conn_max_age=500)
        DATABASES['default'].update(prod_db)



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#### Custom values ####
MAIN_SERIES_NAME = "main"
#########################







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
ALLOWED_HOSTS = ['theengirls.herokuapp.com', '192.168.1.129']
ALLOWED_HOSTS.append('localhost')

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

# https://docs.djangoproject.com/en/3.0/topics/i18n/

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
#STATIC CONFIGURATION
#############################################



STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


STATICFILES_DIRS = (
    # This is where static files for the whole site will be stored
    os.path.join(BASE_DIR, 'theengirls/static/'),
)


#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#EDIA_URL = '/media/'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


DEFAULT_FILE_STORAGE = 'theengirls.storage_backends.MediaStorage' 
