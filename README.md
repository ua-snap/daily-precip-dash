# Daily precipitation visualization app

## Structure

 * `application.py` contains the main app loop code.
 * `gui.py` has most user interface elements.
 * `data.py` has data manipulation / fetch code.
 * `luts.py` has shared code & lookup tables and other configuration.
 * `assets/` has images and CSS (uses [Bulma](https://bulma.io))

## Local development

After cloning this template, run it this way:

```
pipenv install
export FLASK_APP=application.py
export FLASK_DEBUG=True
pipenv run flask run
```

The project is run through Flask and will be available at [http://localhost:5000](http://localhost:5000).

Other env vars that can be set:

 * `DASH_LOG_LEVEL` - sets level of logger, default INFO
 * `ACIS_API_URL` - Has sane default (https://data.rcc-acis.org/StnData?)
 * `DASH_CACHE_EXPIRE` - Has sane default (1 day), override if testing cache behavior.

## Deploying to AWS Elastic Beanstalk:

Apps run via WSGI containers on AWS.

Before deploying, make sure and run `pipenv run pip freeze > requirements.txt` to lock current versions of everything.

```
eb init
eb deploy
```

The following env vars must be set:

 * `REQUESTS_PATHNAME_PREFIX` - URL fragment so requests are properly routed.
 * `GTAG_ID` - Google Tag Manager ID

For local development, set `FLASK_DEBUG` to `True`.  This will use a local file for source data and enable other debugging tools.