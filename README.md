# HBntory — Inventory Management Platform

Team project (Holberton School, BTS SIO) — see `docs/COMPATIBILITY_REPORT.md`
first, it documents an important integration issue the team needs to
resolve before final delivery.

## Structure

```
hbntory/
  ai_service/           AI Query Service (Task 5) — Tété
  client_web/            Client Web Interface (Task 6) — Tété
  backend/                Database + internal/auth API (Task 1, 2) — teammate
  product_mcp_server/     Product MCP Server (Task 4) — teammate
  backoffice/              Backoffice web app (Task 3) — Collins
  docs/                    Shared project documentation
  docker-compose.yml       Starts all services together
```

## Quick start (Docker)

```bash
cp ai_service/.env.example ai_service/.env   # fill in your GROQ_API_KEY
docker compose up --build
```

| Service | URL |
|---|---|
| Backend (DB + auth + internal API) | http://localhost:8000 |
| Backoffice (currently its own separate DB — see report) | http://localhost:8003 |
| Product API (placeholder — swap for the real one, see report) | http://localhost:8001 |
| AI Query Service | http://localhost:8002 |

The `client_web/` static page isn't wired into `docker-compose.yml` (no
build step needed) — serve it separately for now:
```bash
cd client_web && python3 -m http.server 8080
```

## Before you demo or submit

Read `docs/COMPATIBILITY_REPORT.md` — in particular, the Backoffice and
the Backend currently use **two separate databases**, so stock/user
changes made in one won't show up in the other (or in the chatbot's
answers). That needs to be resolved as a team for the demo to make sense
end-to-end.

## Documentation

- `docs/supported_questions.md` — question types the AI Query Service handles
- `docs/communication_strategy.md` — REST/WebSocket/MCP decisions
- `docs/architecture_diagram.md` — system architecture (Collins)
- `docs/COMPATIBILITY_REPORT.md` — integration analysis (start here)
