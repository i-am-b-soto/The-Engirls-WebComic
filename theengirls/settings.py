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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#### Custom values ####
MAIN_SERIES_NAME = "main"
#########################

########### Secret Keys ################
def getSocialInfo(filename):
    with open(filename) as social_secrets:
        line = social_secrets.readline()
        line = line.split(':')
        secrets_tuple = (line[0], line[1])
        return secrets_tuple
    return ('','')

#FB_VALUES = getSocialInfo('facebookkeys.txt')
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY', None) # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET', None)  # App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_URL_NAMESPACE = 'social'



#LOGIN_REDIRECT_URL = '/'
#AUTH_USER_MODEL = 'registration.User'
LOGIN_URL = 'login'
LOGOUT_URL = 'custom_logout'
LOGIN_REDIRECT_URL = 'login'
LOGOUT_REDIRECT_URL = 'custom_logout'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('Django_App_Key', None) 
####################################################




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG_FILE = "Debug_Log.txt"

ALLOWED_HOSTS = ['theengirls.herokuapp.com']
ALLOWED_HOSTS.append('localhost')

# Application definition


INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'ckeditor',
    'ckeditor_uploader',
    'comics',
    'blog',
    'django_filters',
    'social_django',
    'django.contrib.admin',
    'django.contrib.auth',    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware', #<-- Social Django
]


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


###### Django Social-auth #######################

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    #'social_core.backends.instagram.InstagramOAuth2', <-- Appears to be deprecated
    'django.contrib.auth.backends.ModelBackend',
)
####################################################


TEMPLATE_DEBUG = True
WSGI_APPLICATION = 'theengirls.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)



# Password validation
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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

############################################
#STATIC CONFIGURATION
#############################################



STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # This is where static files for the whole site will be stored
    os.path.join(BASE_DIR, 'theengirls/static/'),
)


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
###########################################d

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
 
###################################