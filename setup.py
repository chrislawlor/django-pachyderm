from distutils.core import setup

setup(
    name = "Django Pachyderm",
    version = "0.1a",
    url = 'https://github.com/chrislawlor/django-pachyderm',
    author = 'Chris Lawlor',
    author_email = 'lawlor.chris@gmail.com',
    description = 'Django fields for specialized native DB types..',
    download_url = 'https://github.com/chrislawlor/django-pachyderm/archive/master.tar.gz',
    license = "BSD",
    packages=['pachyderm'],
    package_dir={'pachyderm': 'src/pachyderm'},
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
   ],
)
