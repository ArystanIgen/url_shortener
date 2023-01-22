
# URL Shortener

FastAPI project

To launch project run following command:

```shell
docker compose up -d --build
```

To run test run following command:

```shell
docker compose run app pytest -v --cov . --cov-report term-missing --cov-fail-under=100 --color=yes
```