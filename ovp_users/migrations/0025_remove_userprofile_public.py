# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 14:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_users', '0024_user_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='public',
        ),
    ]