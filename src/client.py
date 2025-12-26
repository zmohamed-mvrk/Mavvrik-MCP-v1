import httpx
import sys
from typing import Dict, Any
from mcp.server.fastmcp import Context
from src.config import settings
from src.security import IdentityManager

class MavvrikClient:
    def __init__(self, ctx: Context):
        self.api_url = settings.api_url
        # Load the headers (API Key + Tenant ID)
        self.headers = IdentityManager.get_auth_headers(ctx)

    async def execute(self, query: str, variables: Dict[str, Any], operation_name: str = "Query") -> Dict[str, Any]:
        """
        Executes GraphQL queries using the Service Account credentials.
        """
        # --- ROBUSTNESS CHECK ---
        # Ensure we are not sending a request without the Tenant Context
        if "x-mavvrik-tenant" not in self.headers and "tenant" not in self.headers:
             raise ValueError("Configuration Error: Tenant ID missing from headers.")

        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            try:
                response = await client.post(
                    self.api_url,
                    json={"query": query, "variables": variables},
                    headers=self.headers
                )
                response.raise_for_status()
                
                payload = response.json()
                
                if "errors" in payload:
                    # Log to stderr for debugging
                    print(f"GraphQL Error in {operation_name}: {payload['errors']}", file=sys.stderr)
                    raise ValueError(f"Mavvrik API Error: {payload['errors'][0]['message']}")
                
                return payload.get("data", {})

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise ValueError("Access Denied: Invalid API Key.")
                if e.response.status_code == 403:
                    # This often happens if the API Key is valid but the Tenant ID is wrong
                    raise ValueError(f"Permission Denied: API Key cannot access tenant '{settings.mavvrik_tenant_id}'.")
                raise ValueError(f"System Error ({e.response.status_code}).")
            
            except httpx.RequestError as e:
                raise ValueError(f"Connection Failed: {str(e)}")