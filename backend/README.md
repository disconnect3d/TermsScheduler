# Terms Scheduler Backend

## Requirements

* Python 3.x
* Dependencies (just fire `pip install -r requirements.txt`)

## Launching project locally

```bash
TODO

python manage.py runserver
```


## Useful info for development

* The app is created in `application.__init__.py`, so that's the place 
where you can look for/register new urls and middlewares.

* All API endpoints by default requires user to be logged in, 
in order to make url being public, decorate it with `public_endpoint`.
