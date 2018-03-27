"""
Settings Local used always for local, production, staging or testing servers
for security purposes
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'partum_inventory',
        'USER': 'root',
        'PASSWORD': '123456'
    }
}

TIME_ZONE = 'Asia/Karachi'
