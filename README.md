# DS5111 YouTube Transcript Processing Pipeline

## Project Core Objective

This project implements a modular streaming data pipeline that processes YouTube video IDs into structured transcript datasets. 
The pipeline validates incoming YouTube IDs, retrieves transcript data through the YouTube Transcript API using a Webshare residential proxy, 
enriches each transcript using Google's Gemini API, validates the resulting JSON record against a predefined schema, 
and outputs structured JSON Lines (JSONL) suitable for downstream analytics and machine learning workflows.

Each stage of the pipeline communicates through standard input (`stdin`) and standard output (`stdout`), allowing the components to be chained together using standard Linux pipes.

---

# Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── bin/
│   ├── clean_ids.py
│   ├── extract_transcripts.py
│   ├── enrich_transcripts.py
│   └── validate_schema.py
├── lib/
├── scripts/
│   ├── init.sh
│   └── init_git_creds.sh
├── tests/
├── Makefile
├── requirements.txt
├── pytest.ini
├── pylintrc
└── README.md
```

---

# Bootstrapping a New Development Environment

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

# Environment Configuration

Create a `.env` file in the repository root.

Example:

```text
GEMINI_API_KEY=your_gemini_api_key
WEBSHARE_PROXY_USERNAME=your_webshare_username
WEBSHARE_PROXY_PASSWORD=your_webshare_password
```

| Environment Variable | Required | Purpose |
|----------------------|----------|---------|
| `GEMINI_API_KEY` | Yes | Authenticates requests to Google's Gemini API during transcript enrichment. |
| `WEBSHARE_PROXY_USERNAME` | Yes (for transcript retrieval) | Username used to authenticate with the Webshare residential proxy. |
| `WEBSHARE_PROXY_PASSWORD` | Yes (for transcript retrieval) | Password used to authenticate with the Webshare residential proxy. |

**Important:** The `.env` file contains sensitive credentials and should never be committed to Git.

---

# Running the Pipeline

Run the YouTube ID validation stage:

```bash
make run
```

This command validates incoming YouTube IDs and outputs only valid IDs.

You may also execute the script manually:

```bash
cat test_ids | env/bin/python3 bin/clean_ids.py
```

To validate the transcript enrichment pipeline:

```bash
make test_enrich
```

---

# Verification

After configuring a new environment, verify that everything is working correctly.

Run the linter:

```bash
make lint
```

Run the automated test suite:

```bash
make test
```

Run the pipeline:

```bash
make run
```

If all three commands execute successfully, the environment has been configured correctly.

---

# Continuous Integration

This repository uses GitHub Actions to automatically perform quality checks on every push and pull request.

The workflow:

- Executes Pylint
- Executes the complete Pytest suite
- Tests against Python 3.11, 3.12, and 3.13
- Verifies the project builds successfully using the project's Makefile

---

# Disaster Recovery

If an AWS EC2 instance or development machine is lost, the project can be rebuilt using only this repository.

1. Launch a new Ubuntu VM or EC2 instance.
2. Configure SSH access to GitHub.
3. Clone the repository.

```bash
git clone <YOUR_GITHUB_REPOSITORY>
cd 2605_DS5111_<YOUR_COMPUTING_ID>
```

4. Initialize the machine.

```bash
bash scripts/init.sh
```

5. Configure Git.

```bash
bash scripts/init_git_creds.sh
```

6. Create the Python virtual environment.

```bash
make env
```

7. Install project dependencies.

```bash
make update
```

8. Create a `.env` file containing the required API credentials.

9. Verify the installation.

```bash
make lint
make test
make run
```

Once these commands complete successfully, the repository has been fully restored and is ready for development.

---

# Technologies Used

- Python
- Linux
- Make
- Git
- GitHub Actions
- Pytest
- Pylint
- Google Gemini API
- YouTube Transcript API
- Webshare Residential Proxy
