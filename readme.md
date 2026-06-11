# Financial Market Data MCP Server

A custom Model Context Protocol (MCP) server that arms AI assistants (like Claude Desktop) with real-time financial market data, advanced quantitative metrics, and programmatic data visualization.

By bridging Large Language Models (LLMs) with an isolated, high-performance Python environment, this server eliminates mathematical hallucinations and gives AI assistants the power to calculate exact risk metrics and render charts on demand.

---

## Core Features

### SDE Architecture Upgrades

* Built-in caching (`lru_cache`) to optimize network requests and prevent Yahoo Finance API rate-limiting.
* Graceful error handling for invalid or unlisted ticker entries.

### Quant Analytics Suite

* Multi-ticker comparison matrices.
* Real-time calculations for complex indicators such as:

  * Relative Strength Index (RSI)
  * Sharpe Ratio

### Data Visualization Pipeline

* In-memory graphing pipeline powered by Matplotlib.
* Generates stock charts and converts them into Base64-encoded strings.
* Charts render natively inside the AI chat interface.

### Production-Ready Deployment

* Fully containerized using Docker.
* Uses interactive standard input/output streams (`STDIN`/`STDOUT`).
* Supports volume mounts for seamless development workflows.

---

## Tech Stack & Tools

* **Core Language:** Python 3.12
* **AI Tool Framework:** FastMCP (Model Context Protocol)
* **Data & Quant Engineering:** Pandas, NumPy, yfinance
* **Data Visualization:** Matplotlib
* **DevOps & Infrastructure:** Docker / Windows Container Engine

---

## Project Structure

```text
finance-mcp-server/
├── server.py            # Main MCP Server code containing tool decorators
├── requirements.txt     # Python production library dependencies
└── Dockerfile           # Blueprint for the isolated Linux container environment
```

---

## Quick Start Setup

### 1. Project Files Configuration

Ensure your `requirements.txt` contains the following libraries:

```text
fastmcp
yfinance
pandas
matplotlib
numpy
```

### 2. Build the Docker Image

Make sure Docker Desktop is running on your machine. Open a terminal in the project directory and execute:

```bash
docker build -t finance-mcp-server .
```

### 3. Link to Claude Desktop Configuration

Open your `claude_desktop_config.json` file (accessible via **Settings > Developer > Edit Config** in Claude Desktop) and add the server configuration under the `mcpServers` block.

Use a volume mount (`-v`) pointing to your live Windows project folder to avoid rebuilding the container whenever you edit code.

```json
{
  "mcpServers": {
    "finance-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "C:\\Users\\YOUR_USERNAME\\PATH\\TO\\finance-mcp-server:/app",
        "finance-mcp-server"
      ]
    }
  }
}
```

---

## Verification & Testing

1. Completely close and restart Claude Desktop (`Ctrl + Q`).
2. Open a fresh chat.
3. Confirm that a tool icon appears in the chat input area, indicating that the MCP tool registry is active.
4. Paste the following test prompt:

```text
Compare the current prices of AAPL, NVDA, and TSLA.
For AAPL, calculate its 14-day RSI and Sharpe Ratio,
and generate a 90-day chart so I can visualize the historical trend.
```

This prompt verifies:

* Real-time market data retrieval
* Quantitative analytics calculations
* Chart generation and rendering
* End-to-end MCP tool execution

```
```
