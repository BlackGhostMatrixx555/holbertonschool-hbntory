# HBntory — System Architecture Diagram
┌─────────────────────────────┐
                                    │      External Users         │
                                    └──────────────┬──────────────┘
                                                   │
                                                   │ REST
                                                   ▼
                                      ┌────────────────────────┐
                                      │ Client Web Interface   │
                                      │ (HTML/CSS/JavaScript)  │
                                      └────────────┬───────────┘
                                                   │
                                                   │ REST API
                                                   ▼
                                      ┌────────────────────────┐
                                      │    AI Query Service    │
                                      │ (LLM + AI Agent)       │
                                      └───────┬────────┬───────┘
                                              │        │
                                   MCP Tools  │        │ SQLAlchemy
                                              │        │
                                              ▼        ▼
                                 ┌────────────────┐  ┌─────────────────┐
                                 │ Product MCP    │  │ SQLite DB       │
                                 │ Server         │  │ Users/Branches  │
                                 └───────┬────────┘  │ Stock           │
                                         │           └────────▲────────┘
                                         │ HTTP REST                   │
                                         ▼                             │
                               ┌────────────────────┐                  │
                               │ External Product   │                  │
                               │ API (Read Only)    │                  │
                               └────────────────────┘                  │
                                                                        │
                                         SQLAlchemy                     │
                                                                        │
                                 ┌──────────────────────────┐           │
                                 │ Backoffice Service       │───────────┘
                                 │ Authentication           │
                                 │ User Management          │
                                 │ Stock Management         │
                                 └────────────▲─────────────┘
                                              │
                                              │
                                 ┌────────────┴─────────────┐
                                 │      Employees           │
                                 │ Admin & Common Users     │
                                 └──────────────────────────┘
cat docs/architecture_diagram.md
