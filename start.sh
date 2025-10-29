#!/bin/bash
set -e

echo "서비스 시작 중"
docker compose up -d

echo "서비스 상태 확인"
docker compose ps

echo "완료"
echo "Swagger 문서: http://localhost:8000/api/docs/swagger/"
