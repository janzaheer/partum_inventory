"""
Settings Local used always for local, production, staging or testing servers
for security purposes
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pis_db',
        'USER': 'root',
        'PASSWORD': 'asfandyar'
    }
}

TIME_ZONE = 'Asia/Karachi'
