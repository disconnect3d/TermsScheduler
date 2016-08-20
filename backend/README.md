# Terms Scheduler Backend

## Requirements

* Python 3.x
* Dependencies (just fire `pip install -r requirements.txt`)

## Launching project locally

```bash
$ python manage.py db upgrade
$ python manage.py runserver
```

# Tests

The tests are written in [`pytest`](http://pytest.org/), 
a full-featured testing tool which doesn't enforce you to write a lot of boilerplate.

As we are using Flask, this is also enhanced by [`pytest-flask`](http://pytest-flask.readthedocs.io/en/latest/) module,
which adds useful [fixtures](http://pytest-flask.readthedocs.io/en/latest/features.html#fixtures) available in your tests.

To launch tests, simply fire:
```bash
$ PYTHONPATH=. py.test

```

## Useful info for development

* The app is created by `create_app` in `application.__init__.py`,
so that's the place where you can look for/register new urls and middlewares.

* All API endpoints by default requires user to be logged in 
(this is due to `require_login` middleware, which is registered in `create_app`), 
in order to make url being public, decorate it with `public_endpoint`.

* The [orm examples](orm_examples.md) contains `python manage.py shell` logs showing 
some usage of `SQLAlchemy`.

