# OSINT Platform 2026 – Гібридна платформа розвідки

Повнофункціональна OSINT-платформа з локальним керуванням (FastAPI), розподіленими воркерами (Celery), PostgreSQL, Redis і сучасним веб-інтерфейсом (Next.js). Готова до деплою через Docker.

> **🐳 Docker Edition**: Весь стек контейнеризований з 3-мільйонною оптимізацією і production-ready конфігурацією.

## 🎯 Ключові можливості

✅ **150+ OSINT-інструментів** інтегровано (Maigret, GeoSpy, Picarta, YouControl, Shodan та ін.)
✅ **Асинхронна обробка** - Celery воркери для паралельної розвідки
✅ **Юридичні докази** - OpenTimestamps, SHA-256 хеші, timestamp-докази
✅ **AI-агенти** - BlacksmithAI, Perplexity, MiniMax для інтелектуального аналізу
✅ **Анонімність** - Tor-інтеграція для конфіденційних операцій
✅ **Веб-интерфейс** - Next.js з Material-UI для зручної роботи
✅ **Безпека** - JWT-автентифікація, rate-limiting, криптування

## 🚀 Швидкий старт (Docker)

### Вимоги
- Docker 20.10+
- Docker Compose 1.29+
- 8GB RAM, 20GB disk

### Установка

```bash
# 1. Клонування
git clone <repo-url> osint-platform-2026
cd osint-platform-2026

# 2. Автоматична конфігурація
bash docker-setup.sh

# 3. Заповнення API-ключів
nano .env

# 4. Запуск
docker-compose up -d

# 5. Доступ
# Фронтенд: http://localhost:3000
# API: http://localhost:8000/docs
# Swagger: http://localhost:8000/redoc
```

## 📂 int-restored / int repo

**Репо:** [fzfw7ckckt-glitch/int](https://github.com/fzfw7ckckt-glitch/int) — osint base pipeline (57 tools)

Відновлений проєкт з архіву `int-main.zip` (відповідає `int-main/` у репо):

```bash
docker-compose -f docker-compose.int.yml up -d
```

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## 📦 Структура проекту

```
osint-platform-2026/
├── Dockerfile.api              # Multi-stage FastAPI
├── worker/Dockerfile           # Multi-stage Celery Worker
├── web/Dockerfile              # Multi-stage Next.js
├── docker-compose.yml          # Production config
├── docker-compose.dev.yml      # Development overrides
├── nginx.conf                  # Reverse proxy (prod)
├── .env.example                # Template конфігурації
├── requirements-api.txt        # Python залежності (API)
├── requirements-worker.txt     # Python залежності (Worker)
│
├── app/                       # FastAPI Backend
│   ├── main.py                # FastAPI entry point
│   ├── models.py              # SQLAlchemy models
│   ├── config.py              # Configuration
│   ├── routers/               # API endpoints
│   └── tasks.py               # Celery tasks
│
├── web/                       # Next.js frontend
│   ├── pages/
│   │   ├── index.tsx
│   │   └── tools.tsx
│   ├── components/
│   └── package.json
│
├── tests/                    # Pytest
├── Makefile                  # Docker commands
└── DEPLOYMENT.md             # Full guide
```

## 🏗️ Архітектура

```
┌─────────────────────────────────────────┐
│   Nginx (HTTPS Reverse Proxy)           │
│   Port: 80, 443                         │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────────┐    ┌────────▼─────┐
│ FastAPI    │    │ Next.js       │
│ :8000      │    │ :3000         │
│ Rate       │    │ Dashboard     │
│ Limiting   │    │               │
└───┬────────┘    └───────────────┘
    │
┌───▼──────────────────────┐
│ Celery Workers           │
│ 4 concurrent tasks       │
│ Chromium + Tor support   │
└───┬──────────────────────┘
    │
┌───┴────────────┬──────────┬──────────┐
▼                ▼          ▼          ▼
PostgreSQL      Redis       Tor       Chrome
DB              Cache       Proxy     Scraping
Port: 5432      Port: 6379  :9050     :3000
```

## 🛠️ Команди

### Makefile

```bash
make setup           # Інішалізація
make up              # Запуск
make down            # Зупинка
make logs            # Логи всіх сервісів
make logs-api        # Логи API
make shell-api       # Bash в контейнері API
make health-check    # Перевірка стану
make test            # Запуск тестів
make clean           # Видалення всього
```

### docker-compose

```bash
docker-compose ps               # Статус сервісів
docker-compose logs -f api      # Логи у real-time
docker-compose exec api bash    # Bash shell
docker-compose restart worker   # Перезапуск воркера
docker-compose up -d --scale worker=3  # Масштабування
```

## ⚙️ Конфігурація

### .env (основні переменні)

```bash
# Безпека
JWT_SECRET_KEY=<32+ symbols>

# База даних
DB_USER=osint
DB_PASSWORD=<strong_password>
DB_NAME=osint

# Redis
REDIS_PASSWORD=<strong_password>

# OSINT API Keys (повний список — .env.example)
SHODAN_API_KEY=
OPENAI_API_KEY=
GEOSPY_API_KEY=
PICARTA_API_KEY=
YOUCONTROL_API_KEY=
```

Детальніше: [USER_GUIDE.md](USER_GUIDE.md) | [.env.example](.env.example)

### Production (з HTTPS)

```bash
# Генерація сертифікатів
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Запуск з Nginx
docker-compose --profile prod up -d
```

## 📊 Інтегровані інструменти

| Категорія | Інструменти |
|-----------|------------|
| **Username** | Maigret, Sherlock, WhatsMyName |
| **Email/Phone** | Hunter, PhoneInfoga, Pipl |
| **Домени** | SpiderFoot, Amass, Shodan, Censys |
| **Сіть** | Nmap, Masscan, Recon-ng |
| **Изобр.** | GeoSpy, Picarta, Forensically |
| **Dark Web** | Ahmia, DarkSearch, OnionLand |
| **Санкції** | OpenSanctions, RuPEP, YouControl |
| **AI** | BlacksmithAI, Perplexity, RevEng |

Всього **150+** інструментів в каталозі.

## 🔐 Безпека

✅ Multi-stage Dockerfiles (30% менше размера)
✅ Non-root контейнери
✅ Network isolation (custom bridge)
✅ Health checks для всіх сервісів
✅ Resource limits
✅ Log rotation
✅ JWT auth + rate limiting
✅ Nginx security headers

## 📈 Масштабування

### Горизонтальное

```bash
docker-compose up -d --scale worker=5
```

### Вертикальное

```yaml
# docker-compose.yml
worker:
  deploy:
    resources:
      limits:
        cpus: '4'
        memory: 4G
```

## 🧪 Розробка

### Mode з Hot Reload

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Включає:
- Hot reload для Python/Node
- pgAdmin (port 5050)
- Redis Commander (port 8081)
- Adminer (port 8080)

### Тестування

```bash
docker-compose run --rm api pytest tests/ -v --cov=app
```

## 📚 Документація

- **Full Guide**: [DEPLOYMENT.md](DEPLOYMENT.md) (12k+ символів)
- **Docker Quick Start**: [DOCKER_README.md](DOCKER_README.md)
- **API Docs**: http://localhost:8000/docs
- **Swagger**: http://localhost:8000/redoc

## 🔧 Troubleshooting

### Порти зайняті?

```bash
lsof -i :8000
lsof -i :3000
kill -9 <PID>
```

### База даних не запускається?

```bash
docker-compose down -v
docker-compose up -d postgres
docker-compose exec api python scripts/init_db.py
```

### Celery не обробляє задачі?

```bash
docker-compose exec worker celery -A app.tasks.celery_app inspect ping
docker-compose restart worker
```

## 💾 Backup & Restore

```bash
# Backup БД
docker-compose exec -T postgres pg_dump -U osint osint | gzip > backup.sql.gz

# Restore
gunzip < backup.sql.gz | docker-compose exec -T postgres psql -U osint osint
```

## 🚢 CI/CD

Включено GitHub Actions:
- ✅ Тестування на push
- 📦 Docker build
- 🔒 Security scanning
- 📤 Registry push

Див. `.github/workflows/ci-cd.yml`

## 📋 Чек-лист для Production

- [ ] Сильні пароліiв в .env
- [ ] Усі API-ключі сконфігуровані
- [ ] JWT secret (32+ chars)
- [ ] HTTPS сертифікати
- [ ] PostgreSQL backups
- [ ] Моніторинг/алертинг
- [ ] Resource limits
- [ ] Firewall правила

## 📞 Контакти

- **GitHub Issues**: [Report Bug](https://github.com/your-repo/issues)
- **Discussions**: [Ask Question](https://github.com/your-repo/discussions)

## 📄 Ліцензія

MIT License - див. LICENSE

---

## ⚡ Швидкий старт

```bash
# 3 команди до запуску
bash docker-setup.sh
nano .env
docker-compose up -d

# Готово!
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
```

**Контейнеризовано для швидкості і надійності. 🚀**
