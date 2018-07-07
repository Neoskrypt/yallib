web: python yallib/manage.py collectstatic --noinput; gunicorn yallib.wsgi —-log-file -
release: flake8 yallib;
worker: celery worker --app=tasks.app;
