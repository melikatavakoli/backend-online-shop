```markdown
<div align="center">

# 🚀 Modular Django Backend

A modular, scalable Django 5 backend designed for **real-world, growing projects**.  
Focused on **clean architecture, async processing, WebSockets, Docker**, and <br>
being actually maintainable when the codebase gets big.

⚠️ This project is still under active development.  
APIs, structure and internals may change.

---

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Django](https://img.shields.io/badge/Django-5.x-0C4B33?style=for-the-badge&logo=django&logoColor=white)]()
[![DRF](https://img.shields.io/badge/DRF-API-red?style=for-the-badge)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()

</div>

---

## 🧩 What This Project Is About

This repo is my attempt to build a **modular backend** that:

- scales beyond just a few apps,
- stays readable when business logic grows,
- supports **REST, WebSockets, background jobs, file storage, and Docker** out of the box,
- can be run **with or without Docker**,
- and is actually pleasant to work with on a daily basis.

It’s still a work-in-progress, but the main building blocks are already here.

---

## 🧱 Architecture Overview

The project follows a **domain-based modular architecture**.  
Each domain lives in its own app and owns its data + logic.

```bash
project
│
├── config          # Global settings and service configuration
├── common          # Shared utilities, base classes, mixins, helpers
│
├── users           # Auth & user management
├── profiles        # Extended user profiles
├── address         # Address and location data
│
├── product         # Products
├── cart            # Shopping cart
├── order           # Orders
├── invoice         # Invoices & billing
├── transaction     # Payment transactions
│
├── course          # Courses and learning content
├── lives           # Live sessions / live content
│
├── blog            # Blog system
├── notifications   # Notifications (in-app / push / etc.)
│
├── chat            # Real-time chat (WebSocket)
├── tickets         # Support tickets
│
├── dashboard       # Admin / dashboard APIs
├── iqplus          # IQPlus-related services
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── manage.py
```

Each app generally has:

- `models/`
- `serializers/`
- `views/`
- `urls/`
- `tasks/`
- `signals/`
- `tests/`
- sometimes `types/` (for enums & typed constants)

Shared / cross-cutting stuff goes into `common/`.

---

## 🛠 Tech Stack

### Core

- **Django 5**
- **Django REST Framework**
- **PostgreSQL**

### Async & Realtime

- **Celery** (background jobs)
- **Redis** (broker / cache)
- **Django Channels** + **Daphne** (WebSockets)

### Authentication

- **SimpleJWT** (JWT auth)
- **Djoser** (auth endpoints)

### Storage

- **MinIO / S3** via `django-storages`
- Ready for object storage deployments

### Background & Monitoring

- **django-celery-beat**
- **Flower** (Celery monitoring)

### API Docs

- **drf-spectacular** (OpenAPI / Swagger-style docs)

### Utilities

- `pandas`
- `openpyxl`
- `persiantools`
- `jdatetime`
- plus some helpers in `common/`

### Deployment

- **Docker / docker-compose**
- **Gunicorn**
- **Uvicorn** (ASGI)

---

## 🐳 Running with Docker (Recommended)

> If you just want to run the whole stack (DB, Redis, app, workers) with one command,  
> this is the easiest way.

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/project.git
cd project
```

### 2️⃣ Build and start containers

```bash
docker compose up --build
```

This should bring up:

- web app
- PostgreSQL
- Redis
- (optionally) Celery worker / beat / Flower depending on your compose file

### 3️⃣ Apply migrations

```bash
docker compose exec web python manage.py migrate
```

### 4️⃣ Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## ⚡ Docker: Using a pip Mirror (Faster Installs)

In the Docker setup, I added support for using a **pip mirror** to speed up package installation  
or to work better behind restricted networks (e.g. inside Iran or locked-down environments).

You can pass a custom **`PIP_INDEX_URL`** as a build argument.

### 🔧 In `Dockerfile` (conceptually)

```dockerfile
# Default to the normal PyPI, but allow override via build args
ARG PIP_INDEX_URL=https://pypi.org/simple
ENV PIP_INDEX_URL=${PIP_INDEX_URL}

# Later in the build step:
RUN pip install --no-cache-dir -r requirements.txt
```

### 🚀 Using it with `docker compose`

```yaml
services:
  web:
    build:
      context: .
      args:
        PIP_INDEX_URL: https://pypi.tuna.tsinghua.edu.cn/simple
```

or from the CLI:

```bash
docker build \
  --build-arg PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
  -t my-django-backend .
```

If you **don’t** set `PIP_INDEX_URL`, it falls back to the normal PyPI index.  
If you **do** set it, all `pip install` calls inside Docker will use your mirror and  
package installation usually becomes much faster ✅

---

## 💻 Running Without Docker

If you prefer to run things locally without containers, that’s also supported.

### 1️⃣ Create and activate a virtualenv

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables

Create a `.env` file in the project root. For example:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/db_name
REDIS_URL=redis://localhost:6379/0
```

(You can adapt the values to your own setup.)

### 4️⃣ Apply migrations

```bash
python manage.py migrate
```

### 5️⃣ Run the development server

```bash
python manage.py runserver
```

---

## 🔄 Celery & Background Workers

To run background tasks and scheduled jobs, start Celery:

### Worker

```bash
celery -A config worker -l info
```

### Beat (scheduler)

```bash
celery -A config beat -l info
```

### Flower (monitoring)

```bash
celery -A config flower
```

You can also wire these into Docker via separate services in `docker-compose.yml`.

---

## 🔌 WebSockets & Realtime Features

WebSocket support is implemented using **Django Channels** (+ ASGI).

Some realtime features:

- 💬 Chat
- 🎫 Live ticket updates
- 🔔 Instant notifications

In production, this is meant to run behind **Daphne/Uvicorn** and a reverse proxy (like Nginx).

---

## 🧪 Tests

The project uses **pytest**.

Run all tests with:

```bash
pytest
```

You can of course extend and organize tests inside each app’s `tests/` module.

---

## 📦 Fixtures (Sample Data)

Some apps include fixtures for easier local development, e.g.:

- `address`
- `blog`
- `course`
- `product`
- `order`
- `iqplus`
- `lives`
- etc.

You can load a fixture like this:

```bash
python manage.py loaddata fixture_name.json
```

---

## 🧠 A Few Architecture Notes

- Business logic tends to live in **services** / **tasks**, not directly in views.
- `types/` (when present) are used for enums and strongly-typed constants.
- `common/` is where shared utilities live: custom pagination, base views, permissions, exceptions, etc.
- Settings are split by environment (e.g. development / production / local) for cleaner deployment.

---

## 📌 Project Status

- ✅ Core structure and main apps are in place  
- 🛠 Features are being actively developed and refined  
- 🔄 Expect breaking changes while things evolve  

---


Feel free to use, modify, and adapt it to your own projects.
```
