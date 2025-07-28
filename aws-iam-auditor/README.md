# AWS IAM Auditor

A command-line tool that scans IAM users for risky or overly permissive policies using the AWS API — or mock data if credentials are missing.

---

## Why I Built This

In cloud environments, overly broad IAM permissions are one of the biggest security risks. This tool helps teams quickly identify IAM users with admin-level or wildcard policies so they can enforce least-privilege access.

Built as part of a DevOps/SRE scripting portfolio to demonstrate:
- Automation mindset  
- Security awareness  
- Production-ready CLI design  
- Clean developer UX

---

## What It Does

- Scans all IAM users and attached policies via the AWS API
- Detects risky policies using wildcard match patterns (e.g., `AdministratorAccess`, `custom-*`, `*admin*`)
- Assigns a **risk level** (`High`, `Medium`, `Low`) to each match
- Automatically falls back to mock data if AWS credentials are missing or invalid
- Outputs results to terminal and also writes to file — `Markdown`, `CSV`, or `JSON`

---

## ✅ Key Features

- [x] Risk tagging based on policy name patterns
- [x] Supports real AWS accounts or safe offline mock data
- [x] Output to Markdown, CSV, or JSON
- [x] Auto-prompt to choose format if not specified
- [x] Custom filename support (e.g. `--output report.csv`)
- [x] Built with `boto3`, `tabulate`, and clean CLI design

---

## Requirements

- Python 3.8+
- `boto3`
- `tabulate`

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

Scan a live AWS account
```bash
python3 auditor.py
```
If valid AWS credentials are found (via aws configure, aws sso login, etc.), the script will pull real user data. Otherwise, it will fallback to local sample data.

### Prompted output (default behavior)
When no format is passed, you'll see:

```lua
Select an output format:
  1. Markdown (.md)
  2. CSV (.csv)
  3. JSON (.json)
Enter format [1–3]:
```
The tool will output to output.md, output.csv, or output.json based on your choice.

### Force sample/mock data
```bash
python3 auditor.py --use-sample
```

Custom output file and format
```bash
python3 auditor.py --format csv --output audit-july.csv
```

### Example Output
```sql
[!] Risky IAM Users Found:

| User        | Policy               | Risk   |
|-------------|----------------------|--------|
| devops-admin | AdministratorAccess | High   |
| ci-bot       | custom-policy-*     | Medium |
| edge-bot     | custom-admin-*      | High   |
```

### Output Files
| Format   | Default File  | Use Case                        |
|----------|---------------|---------------------------------|
| Markdown | `output.md`   | Paste into GitHub or Slack      |
| CSV      | `output.csv`  | Load into Excel or GSheets      |
| JSON     | `output.json` | Feed into other tools or scripts|


### Risk Classification
Policy names are matched using fnmatch with the following default patterns:

| Risk Level | Examples                                      |
|------------|-----------------------------------------------|
| High       | `AdministratorAccess`, `*admin*`, `custom-admin-*` |
| Medium     | `custom-*`, `*policy*`, `custom-backup-*`     |
| Low        | No match — considered safe                    |


### TODO (Next Steps)
Add support for IAM roles and group permissions

Add summary stats by risk level

Option to export multiple formats at once

GitHub Actions automation for scheduled scans

👨‍💻 Author
Ben Hankins