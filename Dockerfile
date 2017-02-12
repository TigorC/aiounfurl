FROM python:3.5
ENV PYTHONUNBUFFERED 1
MAINTAINER Igor Tokarev
RUN mkdir -p /srv/app/
WORKDIR /srv
ADD ./example/requirements.txt /srv/app/requirements.txt
RUN pip install -r /srv/app/requirements.txt
ADD ./example/ /srv/app/
EXPOSE 8080
ENV PYTHONPATH $PYTHONPATH:/srv/app
CMD ["gunicorn", "srv:app", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.worker.GunicornWebWorker"]
