# Local settings for example project.


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Admin Name', 'admin@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'arrayfield', # Or path to database file if using sqlite3.
        'USER': 'clawlor',                             # Not used with sqlite3.
        'PASSWORD': 'toughjeep',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qw*iycb)-8bjd6cayppes=b$-ejxnp7p&amp;0w8j20ug0-d8pweut'

if DEBUG:
    # Show emails in the console during development.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
