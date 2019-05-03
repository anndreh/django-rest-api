# Post and retrieve reviews API

Source code that allow users create and retrieve reviews. The technolgies used in this project are:

 - Python
 - Django / Django-REST-Framework
 - Docker / Docker-Compose
 - Test Driven Development

## Documentation

### How to install and setup

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

### Tests

Executing all tests (unit tests, PEP8 e coverage)
```
docker-compose run --rm app sh -c "coverage run --source='.' manage.py test && flake8"
```

Showing report (coverage - 100%)
```
docker-compose run --rm app sh -c "coverage report"
```

### Admin area to see all data

Django admin page to see users and reviews:
http://localhost:8000/admin/

### API endpoints

Generating Token
```
curl -H "Content-Type: application/json" -d '{"email": "test2@email.com", "password": "123456"}' -X POST http://localhost:8000/api/v1/user/token/
```

Listing reviews from logged user
```
curl -H "Authorization: Token xxx" http://localhost:8000/api/v1/review/review/
```

Creating a new user:
```
curl -H "Authorization: Token xxx" -H "Content-Type: application/json" -d '{
    "title": "Testing rating",
    "ip_address": "127.0.0.8",
    "rating": 1,
    "summary": "Trash Place",
    "submission_date": "2019-05-03",
    "company": "Somewhere"
}' -X POST http://localhost:8000/api/v1/review/review/
```

Partial updating 
```
curl -H "Authorization: Token xxx" -H "Content-Type: application/json" -d '{
    "summary": "Worst Place.",
    "rating": 3
}' -X PATCH http://localhost:8000/api/v1/review/review/5/
```

Complete updating
```
curl -H "Authorization: Token xxx" -H "Content-Type: application/json" -d '{
    "title": "Testing rating",
    "ip_address": "127.0.0.8",
    "rating": 1,
    "summary": "Trash Place",
    "submission_date": "2019-05-03",
    "company": "Somewhere"
}' -X PUT http://localhost:8000/api/v1/review/review/1/
```
