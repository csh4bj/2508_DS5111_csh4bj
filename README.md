# DS5111 YouTube Transcript Processing Pipeline

## Project Overview

This project processes YouTube transcript data through a multi-stage pipeline. 
Raw transcript data is extracted, enriched using the Google Gemini API, 
validated against a predefined schema, and streamed as structured JSON output. 
GitHub Actions automatically runs unit tests and linting to verify the project 
across multiple Python versions.

---

## Setup

These instructions assume a brand-new Ubuntu virtual machine or AWS EC2 instance.

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY>
cd 2605_DS5111_<YOUR_COMPUTING_ID>
```

## 2. Initialize the virtual machine

Run the initialization script to install the required Ubuntu packages.

```bash
bash scripts/init.sh
```

## 3. Configure Git

Configure your Git username and email.

```bash
bash scripts/init_git_creds.sh
```

Verify that the correct username and email are displayed.

## 4. Create the Python virtual environment

```bash
make env
```

This command creates the project's isolated Python virtual environment.

## 5. Install project dependencies

```bash
make update
```

This installs all required Python packages listed in `requirements.txt`.

---

## Environment Variables

Create a `.env` file containing the required API credentials.

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key used for transcript enrichment |
| `WEBSHARE_USER` | Webshare proxy username (used during transcript extraction) |
| `WEBSHARE_PASSWORD` | Webshare proxy password |

---

## Verification

Run the following commands to verify the project is configured correctly:

```bash
make test
make lint
make run
```

To test the transcript enrichment pipeline with the provided sample data:

```bash
make test_enrich
```

Expected results:

- All pytest tests pass.
- Pylint reports a score of **10.00/10**.
- `make run` executes the transcript cleanup pipeline successfully.
- `make test_enrich` validates the enrichment pipeline against the required schema.

---

## Repository Structure

- **bin/** – Pipeline scripts
- **tests/** – Unit tests
- **lib/** – Shared Python package
- **.github/workflows/** – GitHub Actions CI workflow
- **Makefile** – Build, testing, and lint commands
- **requirements.txt** – Python dependencies
- **pytest.ini** – Pytest configuration
- **.pylintrc** – Pylint configuration
- **scripts/** – VM initialization scripts
