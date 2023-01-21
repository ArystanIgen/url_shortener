#!/bin/bash

wait_for () {
    echo "waiting for $1:$2"
    for _ in `seq 0 100`; do
        (echo > /dev/tcp/$1/$2) >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            echo "$1:$2 accepts connections"
            break
        fi
        sleep 1
    done
}

alembic_migration() {
  # alembic revision --autogenerate -m ""
  alembic -x data=true upgrade head
}

update_python_path() {
  export PYTHONPATH="$PYTHONPATH:/src/app"
}

wait_for_db() {
  wait_for "${DB_HOST}" "${DB_PORT}"
}


case "$ENV" in
"LINT")
    echo '===RUN MYPY===' && mypy .
    echo '===RUN FLAKE8===' && flake8 .
    echo '===RUN BANDIT===' && bandit -r .
    echo '===RUN SAFETY CHECK===' && safety check -i 42194
    ;;
"TEST")
    wait_for_db
    pytest -v --cov . --cov-report term-missing --cov-fail-under=100 --isort --color=yes
    ;;
"DEV")
    wait_for_db
    update_python_path
    alembic_migration
    uvicorn app.main:main_app --reload --host 0.0.0.0 --port 8000
    ;;
"PRODUCTION")
    wait_for_db
    update_python_path
    alembic_migration
    python3 gunicorn_server.py
    ;;
*)
    echo "NO ENV SPECIFIED!"
    exit 1
    ;;
esac
