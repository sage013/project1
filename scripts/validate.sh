#!/bin/bash

APP_PORT=5000
APP_URL="http://localhost:$APP_PORT"

echo "[ValidateService] Checking if app is up at $APP_URL..."

# Give the app a few seconds to start (optional backoff)
for i in {1..5}; do
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL")
    if [ "$STATUS_CODE" == "200" ]; then
        echo "[ValidateService] ✅ App is healthy!"
        exit 0
    fi
    echo "[ValidateService] App not responding yet... retrying in 3s ($i/5)"
    sleep 3
done

echo "[ValidateService] ❌ App failed health check. Rolling back."
exit 1
