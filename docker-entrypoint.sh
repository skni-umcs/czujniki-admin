#!/usr/bin/env bash
TYPE=$1
PORT=$2
echo "Starting $TYPE on port $PORT"
sleep 1
python start.py

if [ "$TYPE" = "dev" ]; then
    echo "Running in development mode"
    uvicorn src.rest:app --reload --host 0.0.0.0 --port "$PORT"
else
    echo "Unknown type $TYPE"
    exit 1
fi