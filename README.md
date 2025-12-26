# Mavvrik Cost Intelligence - MCP Server v1

A Model Context Protocol (MCP) server that connects LLMs (like Claude Desktop) to the **Mavvrik FinOps Platform**. This integration allows you to query your cloud costs, visualize trends, and identify top drivers using natural language.

This server provides **read-only** access to Mavvrik cost data. It is designed to answer questions like:

* **Cost Overviews:** "How much did we spend on AWS last month?"
* **Trend Analysis:** "Show me the daily cost trend for the last 30 days."
* **Root Cause Analysis:** "Why did my bill increase from April to May?"
* **Pareto Rankings:** "Who are the top 5 biggest spenders?"
* **Kubernetes Deep Dives:** "Which namespace is driving the cost in my EKS cluster?"

## Prerequisites

* **Python 3.10+** installed.
* A **Mavvrik Account** (Admin access required to generate API keys).
* **Claude Desktop** (or any other MCP-compliant client).

## Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-org/mavvrik-mcp.git](https://github.com/your-org/mavvrik-mcp.git)
    cd mavvrik-mcp
    ```

2.  **Set Up Virtual Environment**
    It is recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### 1. Get Credentials
Log in to your Mavvrik dashboard and navigate to **Settings > API Access** to retrieve:
* `Tenant ID`
* `API Key`

### 2. Configure Environment Variables
**Security Warning:** Never commit your API keys to version control.

Create a `.env` file in the root directory by copying the example:
```bash
cp .env.example .env
