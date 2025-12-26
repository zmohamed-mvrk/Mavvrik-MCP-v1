from mcp.server.fastmcp import Context
from typing import Dict, Any, Optional
import os
from src.config import settings

class IdentityManager:
    @staticmethod
    def get_auth_headers(ctx: Context) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # 1. Primary Auth: Use the API Key + Tenant ID from .env
        # This acts as a "Service Account" for the MCP server.
        api_key = os.getenv("MAVVRIK_API_KEY") or settings.dev_api_key
        tenant_id = os.getenv("MAVVRIK_TENANT_ID") or settings.dev_tenant_id

        if api_key and tenant_id:
            headers["x-api-key"] = api_key
            headers["x-mavvrik-tenant"] = tenant_id
            headers["tenant"] = tenant_id # Legacy compatibility
        else:
            # If these are missing, the query will fail at the backend, 
            # but we log it here for debugging.
            import sys
            print("Warning: MAVVRIK_API_KEY or TENANT_ID missing in .env", file=sys.stderr)

        return headers