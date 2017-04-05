===========
Change log
===========

v0.1.2
-----------
* Introduced changelog
* Updated readme
* Add django as dependency
* Create test structure

v0.1.3
-----------
* Include codeship badge on readme

v0.1.4
-----------
* Fix readme formatting
* Update "forking" readme section
* Update changelog format

v0.1.5
-----------
* Fix install_requires on setup.py

v0.1.6
-----------
* Add sync and async option to mailing
* Create welcome email
* Add id to UserCreateSerializer
* Add basic test cases to UserCreateViewSet and PasswordRecoveryViewSet
* Add test cases to mailing().sendWelcome() and mailing.sendRecoveryToken()
* Add codecov and coverage

v0.1.7
-----------
* Add codecov badge to README.rst
* Test async email triggering
* Fix password hash on user creation
* Password becomes write-only on UserCreateSerializer
* Improved test cases
* Increase test coverage to 100%

v0.1.8
-----------
* Fix conflict with tests when module is installed through pip

v1.0.0
-----------
* Include version badge to README.rst
* Fix test command on README.rst
* Fix password hashing
* Stable current user implementation

v1.0.1
-----------
* Add meta with app_label to models

v1.0.2
-----------
wrongly released version 1.0.1 as 1.0.2.
skipping this version

v1.0.3
-----------
* Test release to check wether tests are included on dist

v1.0.4
-----------
* Update setup.py packages to find_packages()
* Drop distutils in favor of setuptools

v1.0.5
-----------
* Add .egg-info to .gitignore

v1.0.6
-----------
* Distribute templates folder with module

v1.0.7
-----------
* Fix package data distribution

v1.0.8
-----------
* fix readme syntax error

v1.0.9
-----------
* Add phone to user model

v1.0.10
-----------
* Move BaseMail to ovp-core
* Add ovp-core as dependency
* Change emails content to english
* Rename test_coverage to test_execution

v1.0.11
-----------
* Add avatar to user model

v1.0.12
-----------
* Fix dependencies

v1.0.13
-----------
* Fix current user serializer

v1.0.14
-----------
* Add id to UserPublicRetrieveSerializer

v1.0.15
-----------
* Create UserApplyRetrieveSerializer

v1.0.16
-----------
* Include avatar resourcer on Users serializers

v1.0.17
-----------
* Create UserProjectRetrieveSerializer

v1.0.18
-----------
* Asks for current_password when updating user password

v1.0.19
-----------
* Add email to recoveryToken email context

v1.0.20
-----------
* Fix password rehashing whithin multiples saves

v1.0.21
-----------
* Upgrade dependencies

v1.1.0
-----------
* Changed sendRecoveryToken email context. Before:
{'token': self.token, 'email': self.user.email}
Now: {'token': self}
Upgrade path: change email references from 'token' to 'token.token' and 'email' to 'token.user.email'

v1.1.1
-----------
* Set max_length for User.email to 190 so Innodb stops complaining about index size with utf8mb4
* Add user profile feature
* Add locale to emails

v1.1.2
-----------
* Fix requirements

v1.1.3
-----------
* Fix User.uuid migration
* Update UserProfile.user related_name to 'profile'

v1.1.4[unreleased]
-----------
* Add dynamic profile models
* Add slug field. Default is shortuuid
* Add User.public field.
* Remove UserProflie.public field.
* Remove id from UserSearchSerializer
* Rename UserPublicRetrieveSerializer to ShortUserPublicRetrieveSerializer
* Add LongUserPublicRetrieveSerializer
* Replace id with uuid on UserCreateSerializer, UserProjectRetrieveSerializer, UserApplyRetrieveSerializer, ShortUserPublicRetrieveSerializer
* Add PublicUserResourceViewSet
