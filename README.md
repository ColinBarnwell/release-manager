release-manager
===============

Simple release management application, built in the Django framework.


What do you mean by 'release'?
------------------------------

Broadly speaking, a versioned release of a software product.

In this application, there exists the concepts of 'products' and 'packages'.

Both have versioned iterations which can be tracked by the system. The difference
is that a product is a collection of packages. It follows that a product release
is the bringing together of multiple versions of packages.


What do you mean by 'release management'?
-----------------------------------------

In addition to modelling product and package dependencies, this application
has some basic tracking mechanisms. You can set a target date and a manager
for each release, and then track each build.

A build is essentially a QA checklist which is customisable to your own processes.
Examples might be integration testing, translation checks, UAT; even a simple final
sign off.

In this way, a release is a succession of builds, with a successful release
being the successful promotion of the product through each QA checkpoint.

Each build has its own internal number or code (such as beta12).

You can see a full history of each build, and add comments to any event.

Both products and packages have builds, although only products go through the
full release process. Typically a failed release build will require one or
more new package builds. Until a release is successful, packages should be
in a 'provisional' release state.


Quick start
-----------

Some familiarity with [Django](https://www.djangoproject.com/) is required,
particularly in deploying the WSGI application through a web server, and
syncing/migrating the database etc.

This application is optimised for use with [virtualenv](http://virtualenv.readthedocs.org/).
Be sure to *pip install* the appropriate requirements file, found within the
__deployment/requirements__ directory.

You will need to create a server specific settings file, with the
__relman/settings/servers__ directory (use __local_dev.py__ as an example).

You will then need to set the environment variable DJANGO_SERVER_SETTINGS to
the file name you created (do not include the directory).

### Test mode

If you just want to check things out, then simply executing
*python manage.py runserver* will do the trick. Without an environment setting
the application will simply load the __local_dev.py__ settings file.
