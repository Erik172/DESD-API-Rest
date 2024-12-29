#!/bin/sh

# Esperar a que la base de datos esté disponible
while ! nc -z db 5432; do
  echo "Esperando a que la base de datos esté disponible..."
  sleep 1
done

# Crear un archivo de bloqueo para evitar que múltiples instancias inicialicen la base de datos al mismo tiempo
LOCKFILE="/app/migrations/.init.lock"

# Verificar si la base de datos está inicializada
if [ ! -d "migrations/versions" ]; then
  if [ ! -f "$LOCKFILE" ]; then
    touch "$LOCKFILE"
    echo "Inicializando la base de datos..."
    flask db init
    flask db migrate
    flask db upgrade
    python app/scripts/seed.py
    rm "$LOCKFILE"
  else
    echo "Esperando a que otra instancia inicialice la base de datos..."
    while [ -f "$LOCKFILE" ]; do
      sleep 1
    done
  fi
else
  echo "La base de datos ya está inicializada."
fi

exec "$@"