# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='ovp-users',
    version='0.1.0',
    author=u'Atados',
    author_email='arroyo@atados.com.br',
    packages=['ovp_users'],
    url='https://github.com/OpenVolunteeringPlatform/ovp-users',
    download_url = 'https://github.com/OpenVolunteeringPlatform/ovp-users/tarball/0.1.0',
    license='AGPL',
    description='This module has core functionality for' + \
                ' ovp users, such as authentication, user management' + \
                ' password recovery and registration',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
)
