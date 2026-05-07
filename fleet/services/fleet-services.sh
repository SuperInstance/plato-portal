#!/bin/bash
# Fleet Services Installation Script
# Usage: sudo bash fleet-services.sh install|start|stop|restart|status|uninstall

set -e

SERVICES=(
  fleet-health-monitor
  fleet-murmur-worker
  constraint-inference
  intent-inference
  quality-gate-stream
  fleet-ambient-loop
)

SYSTEMD_DIR=/etc/systemd/system
REPO_DIR=/home/ubuntu/.openclaw/workspace/repos

install() {
  for svc in "${SERVICES[@]}"; do
    cp "$REPO_DIR/superinstance/fleet/services/${svc}.service" "$SYSTEMD_DIR/"
  done
  systemctl daemon-reload
  echo "Installed ${#SERVICES[@]} fleet services"
}

start() {
  for svc in "${SERVICES[@]}"; do
    systemctl start "$svc"
    echo "Started: $svc"
  done
}

stop() {
  for svc in "${SERVICES[@]}"; do
    systemctl stop "$svc" 2>/dev/null || true
    echo "Stopped: $svc"
  done
}

status() {
  for svc in "${SERVICES[@]}"; do
    systemctl status "$svc" --no-pager || true
    echo "---"
  done
}

case "$1" in
  install) install ;;
  start) start ;;
  stop) stop ;;
  restart) stop; start ;;
  status) status ;;
  uninstall)
    for svc in "${SERVICES[@]}"; do
      systemctl disable "$svc" 2>/dev/null || true
      rm -f "$SYSTEMD_DIR/${svc}.service"
    done
    systemctl daemon-reload
    echo "Uninstalled all fleet services"
    ;;
  *) echo "Usage: $0 install|start|stop|restart|status|uninstall" ;;
esac
