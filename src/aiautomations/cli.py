from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import time

from aiautomations.core import DataAutomationEngine

engine = DataAutomationEngine()


def cmd_profile(args: argparse.Namespace) -> None:
    for file in args.files:
        print(json.dumps(engine.profile_file(Path(file)), indent=2))


def cmd_generate_script(args: argparse.Namespace) -> None:
    output_script = Path(args.output_script)
    output_script.parent.mkdir(parents=True, exist_ok=True)
    plan = engine.build_plan(args.instruction, [Path(p) for p in args.inputs])
    engine.generate_script(plan, [Path(p) for p in args.inputs], output_script, args.output_data)
    print(f"Generated: {output_script}")
    print("Operations:", ", ".join(plan.operations))


def cmd_run_script(args: argparse.Namespace) -> None:
    subprocess.run(["python", args.script], check=True)


def cmd_pipeline_template(args: argparse.Namespace) -> None:
    template = {
        "name": "example_pipeline",
        "description": "Edit steps and run with aiauto run-pipeline",
        "steps": [
            {"type": "read_csv", "path": "data/input.csv"},
            {"type": "transform_drop_duplicates"},
            {"type": "write_csv", "path": "data/output.csv"},
        ],
    }
    Path(args.path).write_text(json.dumps(template, indent=2))
    print(f"Created {args.path}")


def cmd_run_pipeline(args: argparse.Namespace) -> None:
    for line in engine.run_pipeline(Path(args.pipeline)):
        print(line)


def cmd_diagram(args: argparse.Namespace) -> None:
    engine.generate_pipeline_diagram(Path(args.pipeline), Path(args.output))
    print(f"Diagram written to {args.output}")


def cmd_start_scheduler(args: argparse.Namespace) -> None:
    spec = json.loads(Path(args.schedule_file).read_text())
    print("Scheduler started (Ctrl+C to stop)")
    while True:
        now = int(time.time())
        for job in spec.get("jobs", []):
            every_min = int(job.get("every_minutes", 60))
            if now % (every_min * 60) < 2:
                print(f"Running pipeline: {job['pipeline']}")
                for line in engine.run_pipeline(Path(job["pipeline"])):
                    print(line)
        time.sleep(2)


def main() -> None:
    parser = argparse.ArgumentParser(prog="aiauto")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("profile")
    p.add_argument("--files", action="append", required=True)
    p.set_defaults(func=cmd_profile)

    p = sub.add_parser("generate-script")
    p.add_argument("--instruction", required=True)
    p.add_argument("--inputs", action="append", required=True)
    p.add_argument("--output-script", default="generated/task.py")
    p.add_argument("--output-data", default="generated/output.csv")
    p.set_defaults(func=cmd_generate_script)

    p = sub.add_parser("run-script")
    p.add_argument("script")
    p.set_defaults(func=cmd_run_script)

    p = sub.add_parser("pipeline-template")
    p.add_argument("--path", default="pipeline.json")
    p.set_defaults(func=cmd_pipeline_template)

    p = sub.add_parser("run-pipeline")
    p.add_argument("--pipeline", required=True)
    p.set_defaults(func=cmd_run_pipeline)

    p = sub.add_parser("diagram")
    p.add_argument("--pipeline", required=True)
    p.add_argument("--output", default="pipeline.mmd")
    p.set_defaults(func=cmd_diagram)

    p = sub.add_parser("start-scheduler")
    p.add_argument("--schedule-file", required=True)
    p.set_defaults(func=cmd_start_scheduler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
