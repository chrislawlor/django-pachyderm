
# Example Django Project #

## About ##

Describe example here.

## Prerequisites ##

* Python >= 2.5
* pip
* virtualenv (virtualenvwrapper is recommended for use during development)

## Installation ##

### Creating the environment ###

Create a virtual python environment for the project.
If you're not using virtualenv or virtualenvwrapper you may skip this step.

#### For virtualenvwrapper ####

        mkvirtualenv --no-site-packages example-env

#### For virtualenv ####

        virtualenv --no-site-packages example-env
        source example-env/bin/activate

### Clone the code ###

Obtain the url to your git repository.

        git clone <URL_TO_GIT_RESPOSITORY> example

### Install requirements ###

        cd example
        pip install -r requirements.txt

### Configure project ###
When you're finished installing requirements, you'll need to set up your local settings.py file:

        cp example/settings.py.dist example/settings.py
        vim example/settings.py

### Sync database ###
After you configure your local settings (database, etc.) you're ready to run `syncdb`:

        python manage.py syncdb

## Running ##
Once that's completed you can boot up the dev server:

        python manage.py runserver

Open browser to [http://127.0.0.1:8000](http://127.0.0.1:8000) -- if all went well you should see the "It works!" page.
