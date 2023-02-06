FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt /

RUN apt-get update \
  && apt-get install -y --no-install-recommends graphviz \
  && pip install -r /requirements.txt --use-deprecated=legacy-resolver \
	&& rm -rf /root/.cache

COPY ./ ./

ENV ENVIRONMENT_FILE=".env"

EXPOSE 8085

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "index:server"]
