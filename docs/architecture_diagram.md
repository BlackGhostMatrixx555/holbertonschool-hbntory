# HBntory — Architecture globale

Ce diagramme décrit l'architecture **actuellement implémentée** dans le
dépôt. Les flèches pleines représentent les appels utilisés à l'exécution ;
les flèches pointillées signalent un composant présent mais non intégré au
flux principal.

```mermaid
flowchart LR
    customer[Client final]
    employee[Administrateur / Employé]

    subgraph browser[Interfaces Web]
        client[Client Web<br/>HTML · CSS · JavaScript<br/>:8080]
        backoffice[Backoffice FastAPI<br/>:8003]
    end

    subgraph services[Services applicatifs]
        ai[Service IA FastAPI<br/>POST /api/v1/query<br/>:8002]
        groq[Groq LLM API]
        backend[Backend FastAPI<br/>Auth · Users · Branches · Stocks<br/>:8000]
        mcp[Serveur MCP Produits<br/>Outils FastMCP / stdio]
        products[API Produits<br/>placeholder local<br/>:8001]
    end

    subgraph data[Stockage]
        postgres[(PostgreSQL<br/>Base partagée du backend)]
        sqlite[(SQLite backoffice.db<br/>Base propre au backoffice)]
    end

    customer -->|navigateur| client
    client -->|HTTP JSON<br/>question| ai
    ai -->|API Groq<br/>tool calling| groq
    ai -->|HTTP interne + X-Internal-API-Key<br/>stocks et agences| backend
    ai -->|HTTP REST<br/>catalogue produits| products

    employee -->|navigateur| backoffice
    backoffice -->|SQLAlchemy| sqlite

    backend -->|SQLAlchemy| postgres

    mcp -.->|HTTP REST<br/>catalogue| products
    mcp -.->|HTTP interne + X-Internal-API-Key<br/>stocks et agences| backend
    ai -.->|MCP non utilisé actuellement| mcp
```

## Flux principaux

1. Le client envoie une question depuis le Client Web vers le Service IA.
2. Le Service IA demande au modèle Groq de choisir les données nécessaires.
3. Il interroge directement l'API Produits pour le catalogue et les routes
   internes du Backend pour le stock et les agences.
4. Le Backend lit et écrit dans PostgreSQL.
5. Les administrateurs et employés utilisent le Backoffice, qui gère ses
   propres utilisateurs, agences et stocks dans `backoffice.db`.

## Point d'attention d'intégration

Le Backoffice et le Backend n'utilisent pas la même base de données : le
Backoffice utilise SQLite, tandis que le Backend utilise PostgreSQL. Ainsi,
une modification effectuée dans le Backoffice n'est pas visible dans le
chatbot. De même, le serveur MCP est bien présent, mais le Service IA le
contourne actuellement en appelant directement les API HTTP.

Voir aussi [le rapport de compatibilité](COMPATIBILITY_REPORT.md) pour les
conséquences et les pistes d'intégration.
