<div align="center">

<img src="https://i.imgur.com/lTcSh62.png" alt="Somna Logo" width="500"/>

### 🎵 Listen to background music, white noise, bird singing, and more

API for the Somna application — your personal space with ambient sounds for relaxation, sleep, and focus.

---

## 🚀 Quick Start

**1. Build and start containers**

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
taskiq worker app.core.tasks:broker app.modules.auth.tasks
```

**6. Start the server**

```bash
granian --interface asgi app.main:app
```

## 📖 Documentation

API documentation is available at:

**http://localhost:8000/docs**

---