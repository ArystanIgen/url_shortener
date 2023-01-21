FROM python:3.9.4-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    COLUMNS=200

WORKDIR /src

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 libgomp1 libquadmath0 git

COPY ./src/requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install \
    --no-cache-dir -Ur /src/requirements.txt




COPY ./src /src
CMD ["/src/entrypoint.sh"]
