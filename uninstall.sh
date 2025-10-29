#!/bin/bash
set -e

echo "uninstall 실행."

docker compose down -v --remove-orphans || true

docker system prune -af || true
docker volume prune -f || true

echo "Docker가 모두 제거되었습니다."
echo "완료"
