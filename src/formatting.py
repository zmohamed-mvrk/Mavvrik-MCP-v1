import json
from datetime import datetime
from typing import Any

def format_cost_response(data: Any, title: str, filter_query: str) -> str:
    """
    Standardized formatter for all Mavvrik MCP tools.
    Enforces the 'Context Injection' requirement from the PDF.
    """
    # 1. Header (Context)
    header = (
        f"### {title}\n"
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"**Source:** Mavvrik Intelligence Engine (Net Billable USD)\n"
    )

    # 2. Body (Data)
    if not data or (isinstance(data, list) and len(data) == 0):
        body = "\n> _No cost data found for the specified parameters._\n"
    else:
        # We assume the LLM handles the JSON parsing and explanation.
        # We keep the raw JSON clean for the model to read.
        body = f"\n```json\n{json.dumps(data, indent=2)}\n```\n"

    # 3. Footer (Verification)
    verify_url = f"https://app.mavvrik.ai/cost?{filter_query}"
    footer = (
        f"\n---\n"
        f"🔍 [**Click here to verify this data in the Mavvrik Dashboard**]({verify_url})\n"
    )

    return f"{header}{body}{footer}"