"""
Agent logic for the AI Query Service -- Groq version.

Uses Groq's chat completions API (OpenAI-compatible tool-calling format)
instead of the Anthropic Messages API. Same idea as before: the model
decides which tool(s) to call based on the user's question, instead of a
hand-written if/elif router.

Requires the GROQ_API_KEY environment variable to be set.

Note: Groq periodically retires models -- if MODEL below stops working,
check https://console.groq.com/docs/models for the current list of models
that support tool use, and update the constant.
"""

import json
import os

from groq import Groq

import mcp_client as tools

# If this model is retired, swap it for whatever Groq's docs currently
# list under "tool use" support (e.g. openai/gpt-oss-120b).
MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

_client = None


def _get_client() -> Groq:
    """Lazily create the Groq client so importing this module doesn't
    crash before GROQ_API_KEY is set (e.g. during tests of other parts)."""
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Run: export GROQ_API_KEY=your_key"
            )
        _client = Groq(api_key=api_key)
    return _client

SYSTEM_PROMPT = """You are the HBntory assistant. You answer questions about \
products and stock for a retail company with multiple branches.

Rules you must always follow:
- Only answer using information returned by the tools you are given. Never \
invent product names, descriptions, prices, or stock quantities.
- If a tool returns an error or no data, or a product/branch identifier \
does not exist, say so clearly instead of guessing.
- If the question is outside what your tools can answer (not about \
HBntory's products, stock, or branches), say clearly that it's outside \
what you can help with.
- For shopping-list questions, check the requested quantity against real \
stock and either name the branch(es) that can fulfill the whole list, or \
say clearly that none can.
- Keep answers short and to the point -- a couple of sentences, not a report.
"""

# --- Tool definitions exposed to the model (OpenAI/Groq function format) --
# These mirror the MCP contract in mcp_client_mock.py. When the real
# Product MCP Server (Task 4) is ready, these definitions + the dispatch
# table below are the only things that need to change -- the loop itself
# stays the same.

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_product_details",
            "description": "Get full details (name, description, price, category, supplier) for a single product by its identifier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "Product identifier, e.g. HB-LAP-1001"},
                },
                "required": ["product_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": "Get stock quantities for a product across all branches, or a single branch if branch_id is given.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "branch_id": {"type": "string", "description": "Optional. Restrict to one branch, e.g. BR-1"},
                },
                "required": ["product_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_branch_inventory",
            "description": "List all products and quantities currently in stock at a given branch.",
            "parameters": {
                "type": "object",
                "properties": {
                    "branch_id": {"type": "string", "description": "Branch identifier, e.g. BR-1"},
                },
                "required": ["branch_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_products",
            "description": "List all available products, optionally filtered by category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search products by a keyword matched against the product name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
                "required": ["query"],
            },
        },
    },
]

# Maps a tool name to the actual Python function that implements it.
_DISPATCH = {
    "get_product_details": tools.get_product_details,
    "check_stock": tools.check_stock,
    "list_branch_inventory": tools.list_branch_inventory,
    "list_products": tools.list_products,
    "search_products": tools.search_products,
}

MAX_TOOL_ROUNDS = 5


def answer_question(question: str) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    sources_used = set()

    for _ in range(MAX_TOOL_ROUNDS):
        response = _get_client().chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            max_tokens=500,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return {
                "answer": (message.content or "").strip(),
                "sources": sorted(sources_used),
            }

        # Groq wants to call one or more tools -- execute them and feed the
        # results back in the next round.
        messages.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in message.tool_calls
                ],
            }
        )

        for call in message.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            result = _execute_tool(call.function.name, args)
            sources_used.add(_source_for_tool(call.function.name))
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result),
                }
            )

    return {
        "answer": "I wasn't able to reach a final answer for this question -- please try rephrasing it.",
        "sources": sorted(sources_used),
    }


def _execute_tool(name: str, tool_input: dict) -> dict:
    func = _DISPATCH.get(name)
    if func is None:
        return {"error": "unknown_tool"}
    try:
        return func(**tool_input)
    except Exception as exc:  # noqa: BLE001 -- surface any failure to the model
        return {"error": "tool_execution_failed", "detail": str(exc)}


def _source_for_tool(name: str) -> str:
    return "stock_db" if name in ("check_stock", "list_branch_inventory") else "product_api"
