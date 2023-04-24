#!/usr/bin/env python

from django.apps import AppConfig
from .signals import setup


class DjangoDatabaseCipherConfig(AppConfig):
    name = 'django_database_cipher'

    def ready(self):
        setup()
