#!/bin/bash
# Fleet Health Summary — reads last health tile from PLATO and prints one-line status

PLATO_URL="${PLATO_URL:-http://localhost:8847}"

tile=$(curl -s "$PLATO_URL/room/oracle1_history" 2>/dev/null | tail -c 4096)

if [ -z "$tile" ]; then
  echo "Fleet: UNKNOWN (PLATO unreachable)"
  exit 0
fi

# Extract health status if present
healthy=$(echo "$tile" | grep -o '"healthy":true' 2>/dev/null || true)
degraded=$(echo "$tile" | grep -o '"degraded":true' 2>/dev/null || true)
alerting=$(echo "$tile" | grep -o '"alerting":true' 2>/dev/null || true)

if [ -n "$alerting" ]; then
  echo "Fleet: ALERTING ⚠️"
elif [ -n "$degraded" ]; then
  echo "Fleet: DEGRADED 🟡"
elif [ -n "$healthy" ]; then
  echo "Fleet: HEALTHY ✅"
else
  echo "Fleet: UNKNOWN (no health tile found)"
fi
