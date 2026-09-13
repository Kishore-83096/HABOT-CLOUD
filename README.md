# Student Onboarding Cloud and DevOps Project

## Candidate Information

| Field | Details |
|---|---|
| Name | JAY KISHORE SIRIPURAPU |
| GitHub repository | [HABOT-CLOUD](https://github.com/Kishore-83096/HABOT-CLOUD) |
| Email | kishore.siripurapu1484@gmail.com |
| Phone | 7032057690 |
| Presentation | [Open presentation](https://drive.google.com/file/d/18SYBFIu6mx-FNxxvna2jaC5sh8L5jGwG/view?usp=sharing) |

## Project Overview

This project implements a secure student-onboarding data path for a Django REST Framework application. It demonstrates application validation, local development storage, Terraform infrastructure for Google Cloud, least-privilege IAM, BigQuery row-level security, schema mapping, and a fail-closed GitHub Actions quality gate.

The implementation uses a Python virtual environment and does not require Docker. Because no GCP billing account is available, the application runs in local development mode. Local JSONL files simulate the raw GCS object and staged BigQuery row while Terraform defines the production cloud resources without creating them.

## Architecture and Data Flow

```text
Client
  |
  | POST /api/onboarding/
  v
Django REST Framework serializer
  |
  +--> Invalid payload: HTTP 400, no output written
  |
  +--> Valid payload
          |
          +--> SQLite development database
          +--> D0 raw landing: local_data/d0_raw_landing.jsonl
          +--> D1 staged data: local_data/d1_staged.jsonl

Production target:

Django API -> validation -> GCS D0 raw landing -> BigQuery D1 staged dataset
```

## Directory Structure

```text
habot-project/
|-- app/
|   |-- models.py                 Student onboarding database model
|   |-- dcyn.py                   Deterministic binary validation rules
|   |-- serializers.py            Request validation rules
|   |-- views.py                  POST API endpoint
|   |-- local_pipeline.py         Billing-free local data sinks
|   |-- urls.py                   Application routes
|   |-- migrations/               Django database migration
|   `-- tests/                    API and serializer tests
|-- config/
|   |-- settings.py               Django and local-mode settings
|   |-- urls.py                   Root URL configuration
|   `-- wsgi.py                   WSGI application entry point
|-- schemas/
|   |-- onboarding_schema.json    JSON data contract
|   |-- schema_mapping.csv        Source-to-destination mapping
|   `-- schema_mapping.xlsx       Wrapped-text spreadsheet mapping
|-- tools/
|   `-- create_mapping_workbook.py Reproducible spreadsheet generator
|-- terraform/
|   |-- storage.tf                D0 GCS bucket
|   |-- bigquery.tf               D1 dataset, table, and row policy
|   |-- iam.tf                    Service account and IAM bindings
|   |-- variables.tf              Configurable infrastructure inputs
|   `-- terraform.tfvars.example  Safe configuration template
|-- .github/workflows/
|   `-- quality-gate.yml          Automated security and quality checks
|-- manage.py                     Django command entry point
|-- requirements.txt              Python dependencies
|-- pytest.ini                    Test configuration
|-- .ruff.toml                    Lint configuration
`-- README.md                     Project documentation
```

## Requirements

### Software

- Python 3.12 or later
- Terraform 1.6 or later
- Git
- A GitHub repository for the quality-gate workflow
- GCP billing is not required for local development or Terraform validation

### Project requirements covered

- Terraform configuration for GCS and BigQuery
- GCS uniform bucket-level access and public-access prevention
- BigQuery staged dataset and explicit table schema
- Dedicated service account and least-privilege IAM
- BigQuery row-level access policy
- Django REST Framework schema and validation
- Explicit DCYN binary decision library for deterministic validation
- Source-to-destination data mapping
- JSON schema and serializer consistency test
- Wrapped-text Excel mapping artifact
- Automated tests and linting
- Python formatting verification
- Secret scanning and Terraform security scanning
- Fail-closed CI quality gate
- Failed-build quarantine evidence artifact
- README documentation and presentation evidence

## Implementation Scope

This repository contains the complete application validation flow, deterministic
DCYN rules, local D0/D1 pipeline simulation, schema and mapping artifacts,
Terraform infrastructure definition, automated tests, and fail-closed CI/CD
quality gates requested by the hiring brief.

The cloud resources are defined in Terraform and validated locally. Runtime
deployment is intentionally outside this submission environment; no cloud
resources are created by the validation commands.

## Installation

Open PowerShell and move to the repository root:

```powershell
cd "D:\VENV\HABOT CLOUD\habot-project"
```

Create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

For the current workspace, the environment is located in the parent directory:

```powershell
..\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Validation Commands

Run these commands before pushing to GitHub:

```powershell
python manage.py check
python -m pytest
ruff check app config manage.py
ruff format --check app config manage.py
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
```

Expected results:

```text
Django system check: no issues
Tests: 12 passed
Ruff: All checks passed
Terraform: Success! The configuration is valid.
```

## API Documentation

### Create student onboarding record

```text
POST http://127.0.0.1:8000/api/onboarding/
Content-Type: application/json
```

Request body:

```json
{
  "student_id": "STU-100",
  "student_name": "Test Student",
  "age": 12,
  "has_learning_difficulty": true,
  "support_required": "reading",
  "parent_email": "test@example.com"
}
```

Validation rules:

| Field | Rule |
|---|---|
| `student_id` | Required; must start with `STU-`; maximum 32 characters |
| `student_name` | Required; maximum 120 characters |
| `age` | Required; integer from 1 to 25 |
| `has_learning_difficulty` | Required boolean |
| `support_required` | `reading`, `math`, `speech`, or `none` |
| `parent_email` | Required valid email address |

Successful response:

```text
HTTP 201 Created
```

Invalid data response:

```text
HTTP 400 Bad Request
```

Start the local API:

```powershell
python manage.py migrate
python manage.py runserver
```

Test it from a second PowerShell terminal:

```powershell
$body = @{
    student_id = "STU-100"
    student_name = "Test Student"
    age = 12
    has_learning_difficulty = $true
    support_required = "reading"
    parent_email = "test@example.com"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/onboarding/" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

## Local Development Storage

When `LOCAL_DEVELOPMENT_MODE = True`, a valid request is written to:

```text
db.sqlite3
local_data/d0_raw_landing.jsonl
local_data/d1_staged.jsonl
```

The JSONL files represent the expected shape of the cloud outputs:

- D0 is the raw landing object that maps to Google Cloud Storage.
- D1 is the validated staged record that maps to BigQuery.

Invalid requests are rejected before either JSONL file is created or updated. The generated local files are ignored by Git.

## Cloud Infrastructure

Terraform is located in the `terraform/` directory and is ready for a configured GCP project. It defines:

### D0 raw GCS bucket

- Uniform bucket-level access
- Public access prevention
- GCS access logging to a dedicated security-log bucket
- Object versioning
- Lifecycle cleanup rule
- Environment and data-zone labels

### D1 BigQuery dataset and table

- Explicit student onboarding schema
- Day partitioning on `created_at`
- Deletion protection enabled
- Environment and data-zone labels
- Row-level access policy for support-related records

Terraform uses Google-managed encryption by default. Customer-managed encryption
keys can be introduced through the deployment environment's managed key lifecycle;
no key material is hardcoded or stored in this repository.

### IAM

- Dedicated ingestion service account
- `roles/storage.objectCreator` for raw object creation
- `roles/bigquery.jobUser` for BigQuery jobs
- Dataset-level `roles/bigquery.dataEditor`
- No broad owner or editor role for the ingestion account

Terraform validation does not create cloud resources. To prepare a plan, copy the example variables file and provide environment-specific values:

```powershell
Copy-Item terraform\terraform.tfvars.example terraform\terraform.tfvars
terraform -chdir=terraform plan -var-file=terraform.tfvars
```

Do not run `terraform apply` without a GCP project, billing account, and approved credentials. Never commit service-account keys or real API credentials.

## CI/CD Quality Gate

The workflow at `.github/workflows/quality-gate.yml` runs on pushes and pull requests. It fails closed when a required check fails. The workflow performs:

1. Gitleaks secret scanning
2. Python dependency installation
3. Ruff linting
4. Ruff Python formatting check
5. Pytest execution
6. Terraform formatting check
7. Terraform initialization
8. Terraform validation
9. Checkov Terraform security scanning
10. Failure quarantine evidence upload when the quality gate fails

No security or quality step uses `continue-on-error: true`. A failed check prevents later delivery steps from being treated as successful.

Project evidence includes:

- A failed workflow caused by a deliberately invalid test change or security issue
- A corrected workflow with all checks passing
- The local API response and D0/D1 output files
- Terraform validation output

The direct workflow links below provide the passing and failing pipeline evidence.
Separate pipeline screenshots are not required because each link opens the full
GitHub Actions run, including its status, commit, job, and step results.

Use fake test values only. Never create or commit a real secret for the failure demo.

## Schema and Data Mapping

The JSON contract is in `schemas/onboarding_schema.json`. The source-to-destination mapping is in `schemas/schema_mapping.csv` and the wrapped-text workbook `schemas/schema_mapping.xlsx`. The mapping documents:

- Source field and source type
- Required status
- Validation rule
- Destination field and BigQuery type
- Invalid-data action

The invalid-data policy is to reject the request with HTTP 400 before the record is written to the raw or staged output.

## Deployment Scope

Local mode uses SQLite and JSONL files to exercise the same D0 raw and D1
staged data contracts without external cloud dependencies. Terraform defines
the corresponding GCS, BigQuery, IAM, and row-level security resources for a
configured deployment environment. The repository deliberately does not create
cloud resources during validation.

## Evidence and Presentation

| Evidence | Link |
|---|---|
| Presentation | [Open presentation](https://drive.google.com/file/d/1H3VHNLfmDvP93UFyuYOqj2fp_0_VJLJp/view?usp=drive_link) |
| GitHub Actions page | [Open GitHub Actions](https://github.com/Kishore-83096/HABOT-CLOUD/actions) |
| Passing workflow run | [Open successful run](https://github.com/Kishore-83096/HABOT-CLOUD/actions/runs/34706446582) |
| Failing workflow run | [Open failed run](https://github.com/Kishore-83096/HABOT-CLOUD/actions/runs/34690289869) |



