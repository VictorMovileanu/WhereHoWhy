#### Deployment
* pull code
* optional: collect static files
* `sudo supervisorctl restart wherehowhy`

#### Logs
* Celery: `$HOME/logs/celery.log`
* Nginx: 
  * `$HOME/logs/nginx-access.log`
  * `$HOME/logs/nginx-error.log`
* Gunicorn: `$HOME/logs/gunicorn.log`

#### Setup
Follow instructions from [here](https://simpleisbetterthancomplex.com/series/2017/10/16/a-complete-beginners-guide-to-django-part-7.html)
and in INSTALLATION.md.

#### Celery
Start worker with:
```
celery -A WhereHoWhy worker
```
