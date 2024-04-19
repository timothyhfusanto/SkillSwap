# Most of the set up development is listed on '/skillswap/settings.py' file
# Dependencies are listed in 'requirements.txt' file

1. Create database using mysql connection (database information can be changed that suits your requirements or dependencies):
   
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'skillswap',
            'USER': 'root',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

2. Make migrations:
   # Run the following command on terminal
   "python manage.py makemigrations"
   "python manage.py migrate"

   # Then run the server
   "python manage.py runserver"

3. Create super user to access django admin:
    # Run the following command on terminal
   "python manage.py createsuperuser"

   # Enter the informations that are asked
