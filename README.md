# Post and retrieve reviews API

Source code that allow users create and retrieve reviews. The technolgies used in this project are:

 - Python
 - Django / Django-REST-Framework
 - Docker / Docker-Compose
 - Test Driven Development

## Documentation

## How to install and setup

Docker and docker-compose is required.
To start project, run:

```
docker-compose up
```
To run unit tests:
```
docker-compose run --rm app sh -c "python manage.py test && flake8"
```

The API will then be available at http://localhost:8000

## Tests

Executing all tests (unit tests, PEP8 e coverage)
```
docker-compose run --rm app sh -c "coverage run --source='.' manage.py test && flake8"
```

Showing report (coverage - 100%)
```
docker-compose run --rm app sh -c "coverage report"
```

## Some samples of use

Django admin page to see users and reviews:
http://localhost:8000/admin/

#### API endpoints

Creating a new user:
http://localhost:8000/api/user/create/

Generating new token with login:
http://localhost:8000/api/user/token/
