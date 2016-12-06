==========
OVP Users
==========

.. image:: https://img.shields.io/codeship/b8242540-6d59-0134-3942-5649fa39e129/master.svg?style=flat-square
.. image:: https://img.shields.io/codecov/c/github/OpenVolunteeringPlatform/django-ovp-users.svg?style=flat-square
  :target: https://codecov.io/gh/OpenVolunteeringPlatform/django-ovp-users
.. image:: https://img.shields.io/pypi/v/ovp-users.svg?style=flat-square
  :target: https://pypi.python.org/pypi/ovp-users/

This module implements core user functionality.

Getting Started
---------------
Installing
""""""""""""""
1. Install django-ovp-users::

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
""""""""""""""
If you have your own OVP installation and want to fork this module
to implement custom features while still merging changes from upstream,
take a look at `django-git-submodules <https://github.com/leonardoarroyo/django-git-submodules>`_.

Testing
---------------
To test this module

::

  python ovp_users/tests/runtests.py

Contributing
---------------
Please read `CONTRIBUTING.md <https://github.com/OpenVolunteeringPlatform/django-ovp-users/blob/master/CONTRIBUTING.md>`_ for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
---------------
We use `SemVer <http://semver.org/>`_ for versioning. For the versions available, see the `tags on this repository <https://github.com/OpenVolunteeringPlatform/django-ovp-users/tags>`_. 

License
---------------
This project is licensed under the GNU GPLv3 License see the `LICENSE.md <https://github.com/OpenVolunteeringPlatform/django-ovp-users/blob/master/LICENSE.md>`_ file for details
