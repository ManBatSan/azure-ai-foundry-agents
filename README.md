**Project Title**

AI Foundry Agent Pipeline

---

## Repository

[https://github.com/ManBatSan/azure-ai-foundry-agents](https://github.com/ManBatSan/azure-ai-foundry-agents)

---

## Overview

This repository demonstrates a modular AI agent pipeline built on Azure AI Foundry using the official Python SDK/API. The system comprises four agents:

1. **Researcher**: Performs web searches via Bing using Azure AI Foundry search primitives.
2. **Writer**: Generates draft articles leveraging Foundry language models.
3. **Reviewer**: Evaluates and refines drafts with AI-based checks.
4. **Publisher**: Sends the final article via email.

All components are implemented in Python and orchestrated through a central Foundry orchestrator. This README outlines setup, usage, and a Foundry-centric roadmap.

---

## Prerequisites

* **An Azure subscription** with an AI Foundry resource deployed.
* **Conda** for environment management (Miniconda or Anaconda).
* **Git** installed and repository cloned.

---

## Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ManBatSan/azure-ai-foundry-agents.git
   cd azure-ai-foundry-agents
   ```

2. **Create & activate a Conda environment**:

   ```bash
   conda create -n ai-foundry python=3.9 -y
   conda activate ai-foundry
   ```

3. **Install dependencies** (specifying Foundry SDK version):

   ```bash
   pip install -r requirements.txt
   ```

   Note: Use right now I'm using azure-ai-projects==1.0.0b12 earlier versions had bug realted to authentification.

4. **Environment variables**:

   * Copy `.env.example` to `.env` (not committed to Git).

   * Populate with your credentials and endpoints.

   * The `.env` file is loaded at runtime and **should never** be checked into Git.

5. **Validate Authentification**:

    * Run `az login` and log into your Azure account.

    * Launch the script at `utils/auth_test.py` and verify you can create and delete an agent.
---

## Agents Architecture

Each agent is implemented as a Foundry component under `agents/`:

* `agents/researcher.py`: Uses Foundry search client to fetch results.
* `agents/writer.py`: Calls Foundry LLMs to generate drafts.
* `agents/reviewer.py`: Runs AI-driven quality checks.
* `agents/publisher.py`: Integrates SMTP/SendGrid for email delivery.

Shared utilities (credential loading, logging) live in `agents/utils.py`.

---

## Usage

Run the entire pipeline via the Foundry orchestrator:

```bash
python orchestrator.py --topic "Climate change effects"
```

Or invoke agents individually:

```bash
python agents/researcher.py --query "AI in healthcare"
python agents/writer.py --input ./data/research.json --output ./data/draft.txt
python agents/reviewer.py --input ./data/draft.txt --output ./data/reviewed.txt
python agents/publisher.py --input ./data/reviewed.txt --recipient "user@example.com"
```

---


## License

MIT License. See [LICENSE](LICENSE) for details.
