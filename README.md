# Django api startup

### Introduction

This is a simple django project for HTTP JSON API.


### Main stack

- Web Framework: Django
- Database: PostgreSQL
- Test: Pytest
- Authorization: cancan PyJWT
- Fake data: model-mommy Faker
- Environment: python-dotenv
- Serialization: djangorestfreamwork
- Filter: django-filter


### Getting started

- dotenv sample: see [.env.sample](.env.sample)
- new dotenv for multiple environments, e.g.: `.env.development` `.env.test`
- export environments: `export DJANGO_ENV=.`
- create database and user for current enviroment config
- migrate database: `./manage.py migrate`
- run test: `pytest tests`
