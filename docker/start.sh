#!/bin/bash
#
# Safe start script for CogEngine.
# Checks port 6080 before starting — stops the container if it is the expected
# CogEngine service, aborts if something else is using the port.

set -e

COMPOSE_FILE="$(cd "$(dirname "$0")/.." && pwd)/docker-compose.yml"
PORT=6080
EXPECTED_NAME="cog-engine"   # docker compose project name prefix

existing=$(docker ps --format "{{.Names}}\t{{.Ports}}" \
           | awk -F'\t' -v port="$PORT" '$2 ~ port {print $1}')

if [ -n "$existing" ]; then
    if echo "$existing" | grep -q "$EXPECTED_NAME"; then
        echo "Stopping existing CogEngine container: $existing"
        docker stop "$existing" >/dev/null
    else
        echo "ERROR: Port $PORT is already in use by an unrelated container: $existing"
        echo "Stop it manually before starting CogEngine."
        exit 1
    fi
fi

docker compose -f "$COMPOSE_FILE" up --build -d cogengine
echo ""
echo "Open http://localhost:$PORT/cogengine.html"
