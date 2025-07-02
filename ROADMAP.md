
## Roadmap

Before coding, ensure familiarity with Azure AI Foundry's Python interface for model creation and pipeline orchestration.

* **M0: Pre-commits and Linters** ✅

  * Install and configure pre-commit hooks.

* **M1: SDK & Environment** ✅

  * Install and configure `azure-ai-projects` Python SDK.
  * Verify authentication and connectivity via sample Foundry client calls.


* **M2: Model Generation**

  * Define and deploy LLM resources in Foundry via Python API.
  * Implement `writer.py` with direct Foundry model instantiation.

* **M3: Search Integration**

  * Leverage Foundry search primitives in `researcher.py` for Bing queries.
  * Add result caching and pagination handling.

* **M4: Orchestrator Development**

  * Build `orchestrator.py` using Foundry pipeline constructs.
  * Coordinate agent steps, handle retries and error states.

* **M5: Intelligent Review**

  * Utilize Foundry evaluation models to score drafts.
  * Provide AI-generated feedback and editing suggestions.

* **M6: Publishing Automation**

  * Integrate transactional email SDKs (SMTP or SendGrid).
  * Add status tracking and retry logic.

* **M7: Testing & CI/CD**

  * Write unit tests for agent modules.
  * Configure GitHub Actions to automate builds and deployments.

* **M8: Documentation & Release**

  * Finalize docs, examples, and usage guides.
  * Publish package to PyPI and announce repository.
