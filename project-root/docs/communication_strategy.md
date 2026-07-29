# Communication Strategy — Decision Record

This document covers Task 0.2 of the HBntory project: the communication
strategy chosen for each service-to-service link in the system.

---

## 1. Backoffice — client/interface strategy

**Status: to be decided with the teammate building the Backoffice (Task 3).**

Options on the table (per the subject):
- REST API + a lightweight HTML/CSS/JS frontend
- Server-Side Rendering (SSR)

*Note for the team discussion:* SSR is usually faster to build securely for
an internal admin tool (session-based auth renders naturally, less client-side
state to manage), while REST + JS gives more flexibility if the Backoffice
needs richer interactions later. Given the project's time constraints and
that visual complexity is explicitly not a priority, either is defensible —
what matters is picking one and being able to justify it.

**Decision:** _TBD — fill in once agreed with the Backoffice owner._
**Benefit:** _TBD_
**Trade-off:** _TBD_

---

## 2. Client Web Interface ↔ AI Query Service

**Decision: REST API**

**Benefit:** Each user question is handled independently — the project
explicitly does not require conversation history to be stored or tracked.
REST maps naturally onto this stateless request/response model, and it's
simpler to build, test (curl/Postman), and document with a clear contract
(`POST /api/v1/query`) than a persistent connection would be.

**Trade-off:** No support for streaming the answer token-by-token or pushing
updates without a new request. If the team later wants a "typing" effect or
real-time behavior, this would require adding Server-Sent Events or
switching to WebSockets — acceptable to defer since it's not a project
requirement.

---

## 3. AI Query Service ↔ MCP Tools (Product MCP Server)

**Status: to be finalized with the teammate building the Product MCP Server
(Task 4) — this decision affects both sides and should be locked down
alongside the MCP tool contract (tool names, parameters, response shapes).**

Options on the table:
- **MCP over stdio** — the MCP server runs as a subprocess of the AI Query
  Service (simplest for local/Docker-Compose development, no network layer
  to manage, but ties the two processes' lifecycles together).
- **MCP over HTTP/SSE** — the MCP server runs as its own independent service
  the AI Query Service connects to over the network (matches the project's
  stated architecture better, since the Product MCP Server is listed as a
  separate component, and makes it easier to test the MCP server on its own
  — which Task 4.3 explicitly asks for).

**Recommended decision:** MCP over HTTP/SSE, since the Product MCP Server is
meant to be an independently testable service (Task 4.3: "test your MCP
server manually" before connecting the agent), and the project's suggested
repo structure treats it as its own component alongside the others.

**Benefit:** The MCP server can be started, tested, and debugged
independently of the AI Query Service — matching Task 4.3's requirement —
and it can later be reused by other components if needed.

**Trade-off:** Slightly more setup than an in-process/stdio connection
(needs its own port, its own error handling for connection failures), and
the AI Query Service must handle the case where the MCP server is
unreachable or slow (the Product API itself already simulates this via
`simulate_delay_ms` and `force_error`, so the MCP server should propagate
that failure mode clearly rather than hiding it).

**Decision:** _To confirm with the Task 4 owner._

---

## Summary table

| Link | Decision | Status |
|---|---|---|
| Client Web ↔ AI Query Service | REST | ✅ Confirmed |
| Backoffice interface | REST+JS or SSR | ⬜ To decide (Task 3 owner) |
| AI Query Service ↔ MCP Tools | MCP over HTTP/SSE (proposed) | ⬜ To confirm (Task 4 owner) |
