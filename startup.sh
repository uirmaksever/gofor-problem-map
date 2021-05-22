#!/bin/sh

apt-get update -qq && apt-get install binutils libproj-dev gdal-bin -yqq
gunicorn --env DJANGO_SETTINGS_MODULE="config.settings.production" config.wsgi:application
