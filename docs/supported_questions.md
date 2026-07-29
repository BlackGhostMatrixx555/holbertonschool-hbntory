# AI Query Service — Supported Question Types

This document defines the scope of natural-language questions handled by the
AI Query Service (Task 5). It is written before implementation so that the
agent's behavior can be tested against a clear specification.

## 1. Product details

**Intent:** the user wants information about a specific product (name,
description, price, category, supplier).

**Example questions:**
- "Give me details about product HB-LAP-1001."
- "What is product X?"

**Required tool:** `get_product_details` (Product MCP Server)

**Grounding rule:** if the product identifier does not exist in the Product
API, the agent must say the product was not found — it must not invent a
name, price, or description.

---

## 2. Product availability by branch

**Intent:** the user wants to know which branch(es) currently stock a given
product.

**Example questions:**
- "Which branch has stock of product X?"
- "Where can I find product HB-LAP-1001?"

**Required tools:** `get_product_details` (to confirm the product exists) +
`check_stock` (stock lookup across branches)

**Grounding rule:** if the product exists but has zero stock everywhere, the
agent must say so explicitly rather than staying silent or guessing.

---

## 3. Branch inventory

**Intent:** the user wants to know what is currently available in a specific
branch.

**Example questions:**
- "What products can I find in branch Y?"
- "What's in stock at the Lyon branch?"

**Required tools:** `list_branch_inventory` (stock per branch) +
`get_product_details` or `list_products` (to resolve product names for the
identifiers returned)

**Grounding rule:** if the branch identifier is invalid or unknown, the agent
must say so rather than returning an empty list silently.

---

## 4. Shopping-list recommendation

**Intent:** the user gives a list of products and desired quantities, and
wants to know which branch (or branches) can satisfy the whole list.

**Example questions:**
- "If I want to buy 3 units of X, 2 units of Y, and 4 units of Z, which
  branch or branches should I visit?"

**Required tools:** `check_stock` for each product in the list, aggregated
across branches.

**Expected reasoning:**
1. For each requested product, retrieve stock per branch.
2. Check whether any single branch can satisfy the full list.
3. If not, propose the minimum combination of branches that can.
4. If a product cannot be found or has insufficient total stock anywhere,
   state that clearly instead of silently omitting it.

---

## Out-of-scope questions

Any question that does not map to one of the four categories above (e.g.
questions about pricing history, competitor products, order placement,
delivery, or anything unrelated to HBntory's own catalog and stock) must
receive a clear response stating that the request is outside what the
assistant can help with — never a fabricated answer.

## Non-goals (explicitly out of MVP scope)

- No conversation memory across requests — each question is handled
  independently.
- No user authentication on the client-facing endpoint (public/anonymous).
- No support for placing orders or modifying stock through this interface —
  that remains a Backoffice-only capability.
