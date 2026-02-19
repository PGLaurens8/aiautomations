# aiautomations

A local AI-style data automation CLI inspired by Julius.ai / Powerdrill workflows.

It lets you:
- Profile CSV data quickly.
- Convert natural-language tasks into executable Python scripts.
- Scaffold joins, unions, ETL-like cleanup, and analysis flows.
- Build declarative data pipelines.
- Run scheduled pipeline jobs.
- Generate Mermaid diagrams for pipeline steps.

## Install

```bash
pip install -e .
```

## Quickstart

```bash
# 1) Profile datasets
aiauto profile --files data/customers.csv --files data/orders.csv

# 2) Generate Python from instruction
aiauto generate-script \
  --instruction "Join customers and orders, clean fields, and produce analysis output" \
  --inputs data/customers.csv \
  --inputs data/orders.csv \
  --output-script generated/task.py \
  --output-data generated/output.csv

# 3) Execute generated script
aiauto run-script generated/task.py
```

## Pipeline template

```bash
aiauto pipeline-template --path pipeline.json
aiauto run-pipeline --pipeline pipeline.json
```

## Scheduling

Create `schedule.json`:

```json
{
  "jobs": [
    {"pipeline": "pipeline.json", "every_minutes": 30}
  ]
}
```

Run:

```bash
aiauto start-scheduler --schedule-file schedule.json
```

## Diagrams

```bash
aiauto diagram --pipeline pipeline.json --output pipeline.mmd
```

Render `pipeline.mmd` in any Mermaid-compatible viewer.
