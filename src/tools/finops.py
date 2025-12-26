from collections import defaultdict
from typing import Optional, Literal, List, Any, Dict
from mcp.server.fastmcp import FastMCP, Context
import asyncio

# Internal Imports
from src.client import MavvrikClient
from src.formatting import format_cost_response
from src.config import settings
from src.schemas import CostOption, Filter

# --- GraphQL Constants ---
# We use a single unified query structure consistent with Scenario 1 
QUERY_COSTS = """
query CostsQuery($option: CostOption!, $filter: Filter) {
  costs(option: $option, filter: $filter) {
    cost
    date
    groupId
    groupName
  }
}
"""

QUERY_COST_RANKINGS = """
query CostTopEntriesQuery($option: CostOption!, $filter: Filter) {
  costTopEntries(option: $option, filter: $filter) {
    topEntries {
      cost
      groupId
      groupName
    }
  }
}
"""

QUERY_K8S_COSTS = """
query K8sCostsQuery($option: CostOption!, $filter: Filter) {
  k8sCosts(option: $option, filter: $filter) {
    groupId
    groupName
    cost
    date
  }
}
"""

def register_finops(mcp: FastMCP):
    """
    Registers Financial Operations (FinOps) tools with the MCP server.
    """

    @mcp.tool()
    async def mvk_cost_overview(
        ctx: Context,
        from_date: str,
        to_date: str,
        granularity: Literal["month", "day"] = "month",
        provider: Optional[str] = None
    ) -> str:
        """
        Calculates the single SCALAR total cost (or aggregated bill) for a specific time period.

        [Use Case Strategy]
        - **USE THIS TOOL WHEN:** The user asks for "Total Spend", "How much did we spend?", "What is the bill?", or "Invoice total".
        - **DO NOT USE WHEN:** The user asks for a "breakdown", "trend", "list of services", or "comparison".
        
        [Parameter Reasoning]
        - `granularity`: Default to "month" for high-level reporting. Use "day" only if the user asks for "daily totals" without a chart.
        - `provider`: Use this ONLY if the user explicitly scopes the question (e.g., "Total AWS spend").
        
        [Example Triggers]
        - "What is my total bill for June 2024?" -> from_date="2024-06-01", to_date="2024-06-30"
        - "How much did we spend on GCP last month?" -> provider="gcp"
        """
        client = MavvrikClient(ctx)
        
        # Normalize Provider
        clean_provider = None
        if provider:
            p_map = {"amazon": "aws", "google": "gcp", "microsoft": "azure"}
            clean_provider = p_map.get(provider.lower(), provider.lower())

        try:
            query_filter = Filter()
            if clean_provider:
                query_filter.provider_code = [clean_provider]

            # CRITICAL FIX: Always include groupBy to prevent "undefined" error 
            query_option = CostOption(
                xAxis="date",
                interval=granularity,
                groupBy="provider_code", 
                fromDate=from_date,
                toDate=to_date,
                options=["discount", "tax"]
            )
        except Exception as e:
            return f"Validation Error: {str(e)}"

        variables = {
            "option": query_option.model_dump(exclude_none=True),
            "filter": query_filter.model_dump(exclude_none=True)
        }

        # Execute
        data = await client.execute(QUERY_COSTS, variables, "CostsQuery")
        raw_costs = data.get("costs", [])
        
        # Python-side Aggregation: Sum all groups to get the Total
        total_cost = sum(item.get("cost", 0.0) for item in raw_costs)
        
        # Structure the response for the LLM
        summary_data = {
            "total_cost": round(total_cost, 2),
            "currency": "USD",
            "period": f"{from_date} to {to_date}",
            "grouping_applied": "provider_code (aggregated)"
        }

        return format_cost_response(
            summary_data, 
            "Cost Overview", 
            f"view=overview&provider={clean_provider or 'all'}"
        )

    @mcp.tool()
    async def mvk_cost_trend(
        ctx: Context,
        from_date: str,
        to_date: str,
        granularity: Literal["day", "month"] = "day",
        split_by: Optional[Literal["product_name", "provider_code", "location_id"]] = None
    ) -> str:
        """
        Generates Time-Series data to visualize spending patterns, spikes, or trends over time.

        [Use Case Strategy]
        - **USE THIS TOOL WHEN:** The user asks for "Trend", "Over time", "Daily spend", "Is cost spiking?", or "Graph".
        - **USE FOR DIAGNOSIS:** If user asks "Why did cost go up?", use this FIRST with `split_by` to visualize the driver.

        [Argument Mapping Guide]
        - `split_by="product_name"`: Use if user asks "by Service", "by Product", or "Which service spiked?".
        - `split_by="provider_code"`: Use if user asks "by Cloud", "AWS vs Azure".
        - `split_by="location_id"`: Use if user asks "by Region".
        - `split_by=None`: Use for simple "Total daily spend" trends.

        [Example Triggers]
        - "Show me the daily trend for the last 30 days." -> granularity="day", split_by=None
        - "Plot monthly cost split by Service." -> granularity="month", split_by="product_name"
        """
        client = MavvrikClient(ctx)

        try:
            query_filter = Filter()
            
            # CRITICAL FIX: Ensure valid groupBy exists 
            # If user didn't ask for split, we still group by provider to keep backend happy.
            effective_group_by = split_by if split_by else "provider_code"
            
            query_option = CostOption(
                xAxis="date",
                interval=granularity,
                groupBy=effective_group_by, 
                fromDate=from_date,
                toDate=to_date,
                options=["discount", "tax"]
            )
        except Exception as e:
            return f"Validation Error: {str(e)}"

        variables = {
            "option": query_option.model_dump(exclude_none=True),
            "filter": query_filter.model_dump(exclude_none=True)
        }

        data = await client.execute(QUERY_COSTS, variables, "CostsQuery")
        raw_costs = data.get("costs", [])

        # Post-Processing Logic
        if not split_by:
            # User wanted a simple trend line (Total Cost vs Time).
            # We must merge the provider segments into a single value per date.
            date_map = defaultdict(float)
            for item in raw_costs:
                d = item.get("date")
                c = item.get("cost", 0.0)
                date_map[d] += c
            
            # Convert back to sorted list
            final_costs = [{"date": d, "cost": round(c, 2)} for d, c in sorted(date_map.items())]
        else:
            # User wanted the split, return raw grouped data
            final_costs = raw_costs

        return format_cost_response(
            final_costs, 
            f"Cost Trend ({granularity})", 
            f"view=trend&interval={granularity}&split={split_by or 'total'}"
        )

    @mcp.tool()
    async def mvk_cost_rankings(
        ctx: Context,
        month: str,
        category: Literal["product_name", "service", "resource_group_id", "location_id", "billing_account_id"] = "product_name",
        limit: int = 5
    ) -> str:
        """
        Identifies the TOP cost drivers for a specific month.

        [Use Case Strategy]
        - **USE THIS TOOL WHEN:** The user asks for "Top X", "Biggest spenders", "Rankings", or "Who spent the most?".
        - **DO NOT USE FOR KUBERNETES:** If user mentions "Cluster", "Pod", or "Namespace", use `mvk_k8s_drilldown` instead.

        [Argument Mapping Guide]
        - `category="product_name"`: Default. Use for "Top Services", "Top Products".
        - `category="billing_account_id"`: Use for "Top Teams", "Top Accounts", "Top Subscriptions".
        - `category="location_id"`: Use for "Top Regions".

        [Constraints]
        - Only works for a single `month` (e.g., "2024-06").
        - `limit`: Default is 5. Max is 20.
        """
        client = MavvrikClient(ctx)
        safe_limit = min(limit, settings.max_list_limit)
        formatted_month = f"{month}-01" if len(month) == 7 else month

        try:
            query_filter = Filter()
            # Scenario 3 [cite: 15] uses 'category', 'month', 'limit'.
            query_option = CostOption(
                category=category,
                month=formatted_month,
                limit=safe_limit,
                options=["discount", "tax"]
            )
        except Exception as e:
            return f"Validation Error: {str(e)}"

        variables = {
            "option": query_option.model_dump(exclude_none=True),
            "filter": query_filter.model_dump(exclude_none=True)
        }

        data = await client.execute(QUERY_COST_RANKINGS, variables, "CostTopEntriesQuery")
        
        return format_cost_response(
            data.get("costTopEntries", {}), 
            f"Top {safe_limit} by {category}", 
            f"view=rankings&dim={category}&month={formatted_month}"
        )
    
    @mcp.tool()
    async def mvk_k8s_drilldown(
        ctx: Context,
        from_date: str,
        to_date: str,
        group_by: Literal["cluster_id", "namespace", "node"] = "cluster_id"
    ) -> str:
        """
        Analyzes KUBERNETES (K8s) specific cost metrics.

        [Use Case Strategy]
        - **EXCLUSIVE TRIGGER:** Use this tool IF AND ONLY IF the user mentions "Kubernetes", "K8s", "EKS", "AKS", "GKE", "Cluster", "Node", or "Namespace".
        - **DO NOT USE:** For standard cloud VM/Storage costs (use `mvk_cost_rankings`).

        [Argument Mapping Guide]
        - `group_by="cluster_id"`: "Which cluster costs the most?", "Total K8s spend".
        - `group_by="namespace"`: "Cost by Team" (if on K8s), "Top Namespaces".
        - `group_by="node"`: "Infrastructure cost", "Compute nodes".

        [Example Triggers]
        - "Show me the top namespaces by cost last month." -> group_by="namespace"
        - "What is my K8s cluster spend?" -> group_by="cluster_id"
        """
        client = MavvrikClient(ctx)

        try:
            query_filter = Filter()
            # Scenario 5 [cite: 20] mandates groupBy for K8s queries
            query_option = CostOption(
                xAxis="date",
                interval="month",
                groupBy=group_by,
                fromDate=from_date,
                toDate=to_date
            )
        except Exception as e:
            return f"Validation Error: {str(e)}"

        variables = {
            "option": query_option.model_dump(exclude_none=True),
            "filter": query_filter.model_dump(exclude_none=True)
        }

        data = await client.execute(QUERY_K8S_COSTS, variables, "K8sCostsQuery")
        
        return format_cost_response(
            data.get("k8sCosts", []), 
            f"Kubernetes Cost by {group_by}", 
            f"view=k8s&group={group_by}"
        )
    
    @mcp.tool()
    async def mvk_cost_compare(
        ctx: Context,
        base_start: str,
        base_end: str,
        comp_start: str,
        comp_end: str
    ) -> str:
        """
        Compares total cost between two time periods to calculate VARIANCE (Delta & %).

        [Use Case Strategy]
        - **USE THIS TOOL WHEN:** The user asks "Compare", "Growth", "Increase", "Decrease", or "MoM" (Month-over-Month).
        - **USE FOR "WHY":** If user asks "Why did my bill go up?", use this tool FIRST to establish the exact magnitude of the increase ($ and %).

        [Functional Logic]
        - Calculates: (Base Period Cost - Comparison Period Cost).
        - Returns: Absolute difference ($) and Percentage difference (%).

        [Example Triggers]
        - "Compare June 2024 vs May 2024." -> base=June, comp=May
        - "Did spend go up last week?" -> base=Last Week, comp=Week Before
        """
        client = MavvrikClient(ctx)

        async def fetch_period_total(start, end):
            # Same fix as Overview: Force groupBy="provider_code" to avoid undefined error
            q_opt = CostOption(
                xAxis="date",
                interval="month",
                groupBy="provider_code",
                fromDate=start,
                toDate=end,
                options=["discount", "tax"]
            )
            vars = {
                "option": q_opt.model_dump(exclude_none=True),
                "filter": Filter().model_dump(exclude_none=True)
            }
            res = await client.execute(QUERY_COSTS, vars, "CostsQuery")
            costs = res.get("costs", [])
            # Aggregate manually
            return sum(item.get('cost', 0) for item in costs)

        try:
            base_total, comp_total = await asyncio.gather(
                fetch_period_total(base_start, base_end),
                fetch_period_total(comp_start, comp_end)
            )
            
            delta = base_total - comp_total
            pct = (delta / comp_total * 100) if comp_total != 0 else 0.0
            
            synthetic_data = {
                "comparison": {
                    "base_period": {"start": base_start, "end": base_end, "total_cost": round(base_total, 2)},
                    "comparison_period": {"start": comp_start, "end": comp_end, "total_cost": round(comp_total, 2)},
                    "variance": {
                        "absolute_change": round(delta, 2), 
                        "percent_change": f"{round(pct, 2)}%"
                    }
                }
            }
            return format_cost_response(synthetic_data, "Period Comparison", "view=compare")
            
        except Exception as e:
            return f"Execution Error: {str(e)}"