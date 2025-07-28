# SRE Toolkit (Python + Go)

A growing collection of real-world tools and utilities built for Site Reliability Engineering (SRE), DevOps, and Infrastructure Automation.

This repo showcases a series of small, purpose-built projects written in Python and Go. Each project is fully standalone, tested, and documented for use in real environments or portfolio demonstration.

---

## 📦 Projects

| Project | Description | Status |
|--------|-------------|--------|
| `log-alert-agent` | Parses logs, classifies alerts, and exports summaries in real-time | ✅ Completed |
| `aws-iam-auditor` | Scans IAM policies and flags overly permissive rules | ✅ Completed |
| `...` | More projects coming soon | 🔧 In progress |

---

## 💼 Why This Exists

This toolkit was built as part of a structured portfolio to demonstrate:
- Automation mindset
- Tool-building capability
- Production readiness
- Deep SRE/DevOps skills

Each project is:
- Fully documented
- CLI-driven
- Written with test coverage and clean design

---

## Setup

Each project has its own README and can be run independently.

#### For Python-based tools:

```bash
cd log-alert-agent
pip install -r requirements.txt
python agent.py ...
```

#### Go-based tools can be run via:

```bash
cd some-go-tool
go run main.go
```

## About the Author
Built by Ben Hankins, a Site Reliability Engineer with a passion for automation, reliability, and building clean, purposeful tools that help engineers move faster.

## Coming Soon
Container scanning tool (Go)

Config linter

Deployment diff visualizer

Integration with GitHub Actions and AWS
