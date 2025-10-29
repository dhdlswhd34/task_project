# 과제용 프로젝트

이 프로젝트는 Django REST Framework 기반의 **시험 응시 및 수업 수강 신청 시스템** 입니다.


## 구조
  
> Nginx → Gunicorn → Django → PostgreSQL

| 구성 요소 | 역할 |
|------------|------|
| **Nginx** | 요청 라우팅 및 정적 파일 서빙 |
| **Gunicorn** | Django WSGI 서버 |
| **Django (DRF)** | REST API 서버 (JWT 인증 / Swagger 문서 제공) |
| **PostgreSQL** | 데이터베이스 |
| **Docker Compose** | 컨테이너 오케스트레이션 |

---

## 실행 방법

### 1 프로젝트 클론

```bash
git clone https://github.com/dhdlswhd34/task_project.git
cd task_project
```

### 2 설치 및 실행

```bash
chmod +x install.sh
./install.sh
```

> **install.sh** 스크립트는 다음을 자동으로 수행합니다:
> - 기존 컨테이너 및 볼륨 정리  
> - Docker 이미지 새로 빌드  
> - Django 마이그레이션 실행  
> - Seed 데이터 자동 로드 (기본 사용자, 시험, 수업, 결제 생성)

---

## API 문서
| 항목 | 주소 |
|------|------|
| **Swagger 문서** | [http://localhost:8000/docs/swagger](http://localhost:8000/docs/swagger) |
| **ReDoc 문서** | [http://localhost:8000/docs/redoc](http://localhost:8000/docs/redoc) |

---

## 초기 데이터 (Seed)

| 항목 | 예시 데이터 |
|------|--------------|
| **사용자** | `test1@example.com`, `test2@example.com`, `test3@example.com` <br> (비밀번호: `1234`) |
| **시험** | `진행 중 시험`, `시작 전 시험`, `종료된 시험` (각각 3개) |
| **수업** | `진행 중 수업`, `시작 전 수업`, `종료된 수업` (각각 3개) |
| **결제** | 사용자별 자동 생성 (시험/수업 1건씩) |

---


## 🧰 기술 스택

| 구분 | 기술 | 버전 / 설명 |
|------|------|--------------|
| Backend Framework | Django REST Framework | Django 5.1.2 / DRF 3.15 |
| Auth | SimpleJWT | Access / Refresh Token 기반 |
| API Docs | drf-spectacular | Swagger / ReDoc 문서 자동화 |
| Database | PostgreSQL | 15.x |
| Container | Docker, docker-compose | 컨테이너 기반 배포 환경 |
| Language | Python | 3.12 |
| OS | Ubuntu | 22.04 (Docker 기반) |

---
