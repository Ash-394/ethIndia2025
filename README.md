# ETHOS

**An advanced multi-agent system for cumulative intelligence analysis, built on the ASI Alliance stack and integrated with Flow and Filecoin for decentralized operation and verifiable evidence storage.**

[Project Demo Link]() &nbsp;&nbsp;•&nbsp;&nbsp; [github.com/Ash-394/ethIndia2025]

---

## Project Summary

ETHOS is a decentralized, multi-agent system designed to assist human analysts in complex investigations. It addresses the critical challenge of synthesizing a coherent narrative from a continuous stream of unstructured, text-based intelligence. The platform leverages a stateful, cumulative architecture, allowing its understanding of a case to grow more sophisticated with each new piece of evidence.

## Core Innovation: Hybrid Reasoning

The central innovation is a **hybrid reasoning architecture** that combines a formal logic engine with a powerful LLM. This creates a final output that is both creatively insightful and logically sound.

1.  **AI for Translation:** An initial agent uses **ASI:One** to handle the "fuzzy" task of translating unstructured English reports into a structured, formal **MeTTa** script of facts.
2.  **MeTTa for Logic:** A specialist agent then uses this script to build a cumulative knowledge base, executing a ruleset and complex queries to produce verifiable, logical insights.
3.  **AI for Synthesis:** Finally, the system feeds the raw evidence and the MeTTa findings into a second **ASI:One** prompt to generate a high-level, intuitive theory of the case.

## System Architecture

The system is a decentralized, two-agent collaboration:

-   **Collector Agent:** Serves as the system's public interface. It ingests tips via a live webhook, uses ASI:One to create a MeTTa script, archives the evidence to **Filecoin via Lighthouse**, and forwards the complete MeTTa script to the Detective.

-   **Detective Agent:** The analytical core. It receives the MeTTa script, loads it into its **MeTTa** reasoning space to generate logical facts, and then uses **ASI:One** to synthesize all available information. The final report is then pushed to clients via a WebSocket and a summary is logged on the **Flow blockchain**.

## Web3 Integration

This project is built as a Web3-native application, utilizing decentralized technologies for security, persistence, and transparency.

#### Decentralized Storage: Filecoin & Lighthouse
To ensure the integrity and persistence of evidence, our Collector Agent uses **Lighthouse** to store all incoming tips and evidence files on the **Filecoin Calibration Testnet**. This provides a meaningful, decentralized storage solution for critical case data, protecting it from tampering and ensuring long-term availability.

#### On-chain Verification: Flow EVM Testnet
The system is built on **Flow** and interacts with the blockchain to provide a transparent, on-chain record of investigative summaries.
-   **Network:** Flow EVM Testnet
-   **Deployed Contract Address:** `[Your Deployed Contract Address on Flowscan]`
    -   *(Note: The contract was deployed in transaction `0x8c601859c86547d38bce138ac49bb47accd96bfe4c32d6b4d289795d0a1fda89`)*

## Technology Stack

| Category              | Technology                                   |
| --------------------- | -------------------------------------------- |
| **Agent Framework**   | Fetch.ai uAgents                             |
| **AI & LLM**          | ASI:One                                      |
| **Logical Reasoning** | MeTTa (hyperon-experimental)                 |
| **Smart Contracts**   | Flow EVM Testnet                             |
| **Decentral Storage** | Filecoin (via Lighthouse)                    |
| **API & Webhooks**    | FastAPI, Uvicorn, WebSockets                 |

## Getting Started

#### 1. Prerequisites
- Python 3.10+
- A virtual environment tool (`venv`)

#### 2. Installation & Setup
```bash
# Clone the repository
git clone [github.com/Ash-394/ethIndia2025]
cd [agents/fetch-agents]

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configuration
Create a file named `.env` in the root directory and add your ASI Alliance API key:
```
ASI_API_KEY="your_key_here"
```

#### 4. Execution
The system requires three separate terminals to run.

-   **Terminal 1: Start the Collector Agent**
    ```bash
    python3 evidence_collector.py
    ```
-   **Terminal 2: Start the Detective Agent**
    ```bash
    python3 detective_agent.py
    ```
-   **Terminal 3: Interact with the System**
    Open the `index.html` file in a browser, or use `curl` to send a tip to the live webhook.
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"case_id": "CASE-101", "text": "A new witness saw a blue car leaving the scene."}' \
    [http://127.0.0.1:8003/submit_tip](http://127.0.0.1:8003/submit_tip)
    ```
