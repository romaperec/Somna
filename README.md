<div align="center">

<a href="https://iimg.su/i/t45Cob">
  <img src="https://s6.iimage.su/s/14/gt45CobxHkqovmjdDF9jnoPcuIHtYN4f0iUPti158.png" alt="Somna Logo" width="480"/>
</a>

### 🎵 Background music, white noise, birdsong and more

**API for the Somna application — your personal space of ambient sounds for relaxation, sleep and focus.**

<p>
  <img src="https://img.shields.io/badge/python-3.13%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.13+"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy 2.0"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Redis-FF4438?style=flat-square&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/NATS%20JetStream-27AAE1?style=flat-square&logo=natsdotio&logoColor=white" alt="NATS JetStream"/>
</p>
<p>
  <img src="https://img.shields.io/badge/TaskIQ-2563eb?style=flat-square" alt="TaskIQ"/>
  <img src="https://img.shields.io/badge/uv-DE5FE9?style=flat-square" alt="uv"/>
  <img src="https://img.shields.io/badge/Ruff-000000?style=flat-square&logo=ruff&logoColor=white" alt="Ruff"/>
  <img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="pytest"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/license-MIT-2f7cf6?style=flat-square" alt="MIT License"/>
</p>

---

## 🌙 About the Service

**Somna** is a web application for background sound: rain, thunderstorms, wind, campfire, ocean waves, morning forest, birdsong and white noise. It helps you relax, fall asleep or stay focused: listen to ready-made sounds, build your own mixes with per-track volume control, and upload your own audio files.

This repository is the **Somna backend**: an asynchronous REST API built with FastAPI, featuring a full authentication cycle, user profiles and audio storage.

---

## 🚀 Quick Start

**1. Build and start containers** (PostgreSQL, Redis, NATS)

```bash
docker-compose up --build
```

**2. Install uv**

```bash
pip install uv
```

**3. Install dependencies**

```bash
uv sync
```

**4. Apply database migrations**

```bash
alembic upgrade head
```

**5. Start the TaskIQ worker**

```bash
taskiq worker app.core.broker:broker app.modules.auth.tasks
```

**6. Start the server**

```bash
granian --interface asgi app.main:app
```

---

## 📖 Documentation

Interactive API documentation (Swagger UI) is available at:

**http://localhost:8000/docs**

---

## 🧪 Tests & Linting

```bash
# Run tests
pytest

# Lint the code
ruff check .

# Format the code
ruff format .
```

---

📄 Distributed under the **MIT License**

</div>
