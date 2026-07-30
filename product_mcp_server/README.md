# HBntory Product & Stock MCP Server

Ce serveur MCP (Model Context Protocol) sert de passerelle entre l'Agent IA et :
1. **L'API Produits externe** (Docker, données produits en lecture seule).
2. **L'API Interne du Backend FastAPI** (Données de stock par agence).

## Outils (MCP Tools) Exposés

| Nom de l'outil | Description | Paramètres |
|---|---|---|
| `get_product_details` | Récupère la fiche complète d'un produit depuis l'API Produit. | `product_id: str` (ex: `"HB-LAP-1001"`) |
| `list_products` | Liste l'ensemble du catalogue produit. | Aucun |
| `check_stock` | Interroge le stock d'un produit sur toutes les agences. | `product_id: str` |
| `list_branch_inventory` | Liste l'inventaire complet d'une agence. | `branch_identifier: str` (ex: `"Paris"`, `"1"`) |
| `list_branches` | Liste les agences physiques configurées. | Aucun |

## Utilisation par l'Agent IA (Collègue 3)

Pendant le développement local, votre collègue peut importer directement le module client :
```python
import client as tools

# Exemples
details = tools.get_product_details("HB-LAP-1001")
stock = tools.check_stock("HB-LAP-1001")
```

En production ou conteneurisé via Docker, l'agent IA se connecte au serveur MCP via STDIO ou SSE.
