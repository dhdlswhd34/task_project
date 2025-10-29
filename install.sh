#!/bin/bash
set -e

echo "[1/4] 초기화"
docker compose down -v --remove-orphans || true
docker builder prune -af || true

echo "[2/4] requirements.txt 및 이미지 빌드"
docker compose build --no-cache

echo "[3/4] 컨테이너 실행 및 초기 마이그레이션 수행"
docker compose up -d
docker compose exec web python manage.py makemigrations task_models
docker compose exec web python manage.py migrate

echo "[4/4] Seed 데이터 생성"
docker compose exec -T web python manage.py shell < seed.py

echo "완료!"
echo "Swagger 문서: http://localhost:8000/api/docs/swagger/"
