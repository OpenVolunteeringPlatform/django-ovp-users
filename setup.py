# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='ovp-users',
    version='1.0.0',
    author=u'Atados',
    author_email='arroyo@atados.com.br',
    packages=['ovp_users'],
    url='https://github.com/OpenVolunteeringPlatform/ovp-users',
    download_url = 'https://github.com/OpenVolunteeringPlatform/ovp-users/tarball/1.0.0',
    license='AGPL',
    description='This module has core functionality for' + \
                ' ovp users, such as authentication, user management' + \
                ' password recovery and registration',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = [
      'Django>=1.10.1,<1.11.0',
      'djangorestframework>=3.4.7,<3.5.0',
      'djangorestframework-jwt>=1.8.0,<1.9.0',
      'python-dateutil>=2.5.3,<2.6.0',
      'codecov>=2.0.5,<2.1.0',
      'coverage>=4.2,<4.3.0'
    ]
)
