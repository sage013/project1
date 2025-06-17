#!/bin/bash

APP_PORT=5000
APP_URL="http://localhost:$APP_PORT/tasks"  # Changed to /tasks

echo "[ValidateService] Checking if app is up at $APP_URL..."

for i in {1..5}; do
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL")
    if [ "$STATUS_CODE" == "200" ]; then
        echo "[ValidateService] ✅ App is healthy!"
        exit 0
    fi
    echo "[ValidateService] App not responding yet... retrying in 5s ($i/5)"
    sleep 5
done

echo "[ValidateService] ❌ App failed health check. Rolling back."
exit 1

