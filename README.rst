=====
OVP Users
=====

This module implements core user functionality.

Quick start
-----------
1. Install django-git-submodules::

    pip install ovp-users

2. Add it to `INSTALLED_APPS` on `settings.py`

3. Add `rest_framework_jwt` to `INSTALLED_APPS`

4. Set up REST Framework Authentication::

   # Rest framework

   REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.SessionAuthentication',
       'rest_framework.authentication.BasicAuthentication',
       'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
     )
   }

   # User models

   AUTH_USER_MODEL = 'ovp_users.User'



Forking
-----------
If you have your own OVP installation and want to fork this module
to implement custom features while still merging changes from upstream,
read Forking section on the wiki.
