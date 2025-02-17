# changelogllm

# Changelog LLM 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

**Changelog LLM** is an AI-powered tool that works alongside Dependabot to analyze dependency updates, review changelogs, and intelligently approve or request changes in PRs. It uses LLMs (e.g., GPT-4, Claude) to parse unstructured changelogs, detect breaking API changes, and flag risks in your codebase.

---

## Features

- 🔍 **Changelog Analysis**: Automatically fetches and parses changelogs for updated dependencies.
- 🤖 **LLM-Powered Insights**: Uses AI to identify breaking changes, deprecations, and risks.
- ✅ **PR Review**: Comments on Dependabot PRs with actionable feedback (approve, request changes, or warn).
- 🛠️ **Codebase Scanning**: Statically analyzes your code to check if deprecated APIs are used.
- ⚙️ **Configurable Rules**: Define custom rules for critical dependencies or ignore false positives.

---

## How It Works

1. **Dependabot creates a PR** for a dependency update.
2. **Changelog LLM**:
   - Fetches the changelog/release notes for the new version.
   - Uses an LLM to extract breaking changes and API deprecations.
   - Scans your codebase to check if affected APIs are used.
3. **Post a Review**:
   - Approve the PR if no risks are detected.
   - Request changes with code snippets and remediation steps.
   - Add warnings for minor issues.

---

## Quick Start

1. **Add Configuration**:
   Create `.github/changelog-llm/config.yaml`:
   ```yaml
   # Example config
   llm_provider: "openai"  # or "anthropic", "ollama"
   target_files:
     - "requirements.txt"
     - "pyproject.toml"
   critical_dependencies:
     - "django"
     - "requests"
GitHub Action Setup:
Add .github/workflows/changelog-llm.yml:

yaml
Copy
name: Changelog LLM Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Changelog LLM
        uses: your-username/changelog-llm@v1
        env:
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
Configuration
Key	Description
llm_provider	LLM service (openai, anthropic, or ollama for local models).
critical_dependencies	List of dependencies to treat as high-priority (e.g., security-critical).
ignore_dependencies	Dependencies to skip analyzing (e.g., dev-packages).
auto_approve_minor	Automatically approve non-breaking semver-minor updates.
Contributing
PRs welcome! See CONTRIBUTING.md for guidelines.

Copy

---

# `INSTRUCTIONS.md`

```markdown
# Changelog LLM Setup Guide

## Prerequisites

1. **Python 3.10+** (for CLI/local usage).
2. **GitHub Repository** with Dependabot enabled.
3. **LLM API Key** (e.g., OpenAI, Anthropic, or a local Ollama instance).

---

## Step 1: Create a GitHub App

1. Go to **GitHub Settings > Developer Settings > GitHub Apps**.
2. Create an app with permissions:
   - **Pull Requests**: Read/Write
   - **Contents**: Read
3. Install the app on your repository.

---

## Step 2: Set Up Secrets

Add these secrets to your GitHub repository (`Settings > Secrets > Actions`):

- `LLM_API_KEY`: API key for your LLM provider.
- `GITHUB_TOKEN`: Auto-generated token for GitHub access.

---

## Step 3: Add the Workflow

Create `.github/workflows/changelog-llm.yml`:
```yaml
name: Changelog LLM Review
on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install Changelog LLM
        run: pip install changelog-llm
      - name: Analyze PR
        run: changelog-llm review --pr ${{ github.event.pull_request.number }}
        env:
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
Step 4: Customize Behavior
Edit .github/changelog-llm/config.yaml:

yaml
Copy
# Example: Only analyze major version updates
llm_provider: "openai"
auto_approve_minor: true
critical_dependencies:
  - "django"
  - "sqlalchemy"
How It Reviews PRs
For a Dependabot PR updating requests from 2.30.0 to 2.31.0:

Fetch Changelog:

Checks PyPI/GitHub for release notes.

LLM Analysis:

Asks the LLM: "Does this changelog include breaking changes?"

Code Scan:

Uses AST parsing to check usage of deprecated APIs.

Post Review:

If safe: Approve with ✅.

If risky: Request changes with code snippets.

Example Output
PR Comment Example

Local Development
Clone the repo:

bash
Copy
git clone https://github.com/your-username/changelog-llm.git
cd changelog-llm
pip install -e .
Test against a PR:

bash
Copy
changelog-llm review --pr 123 --local
Copy

---

### Key Files to Create:
1. `.github/changelog-llm/config.yaml` – Configuration.
2. `.github/workflows/changelog-llm.yml` – GitHub Action.
3. `requirements.txt` – Python dependencies (include `openai`, `pygithub`, `requests`).

Let me know if you want help writing the actual Python code or refining the logic! 🚀
