#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-mysql-mysqldump-tab-path}"
export PYTHONUNBUFFERED=1

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

echo "== prepare work dirs =="
mkdir -p work/tabdir work/oracle
find work -type f -name '*.sql' -delete || true
find work -type f -name '*MYSQL-DUMP-TAB-TRAVERSAL-WITNESS*' -delete || true

echo "== docker compose down (clean) =="
down

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 5); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 8
  down
done
if [[ "${up_ok}" != 1 ]]; then
  echo "FAIL mysql-mysqldump-tab-path compose-up-failed MYSQL-DUMP-TAB-TRAVERSAL-WITNESS" | tee poc-last-run.txt
  down
  exit 1
fi

echo "== wait for stub TCP 127.0.0.1:18610 and 18611 =="
ok=0
for i in $(seq 1 60); do
  if python3 - <<'PY'
import socket
for port in (18610, 18611):
    s = socket.create_connection(("127.0.0.1", port), 2)
    s.close()
PY
  then
    ok=1
    echo "stub-ready attempt=${i}"
    break
  fi
  echo "stub-wait attempt=${i}"
  sleep 1
done
if [[ "${ok}" != 1 ]]; then
  echo "FAIL mysql-mysqldump-tab-path stub-not-ready MYSQL-DUMP-TAB-TRAVERSAL-WITNESS" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --tail=80 || true
  down
  exit 1
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL mysql-mysqldump-tab-path poc-exit=${rc} MYSQL-DUMP-TAB-TRAVERSAL-WITNESS" >> poc-last-run.txt
  rc=1
fi

down
exit "${rc}"
