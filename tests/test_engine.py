from pathlib import Path
import json

from aiautomations.core import DataAutomationEngine


def test_build_plan_detects_join_and_pipeline() -> None:
    engine = DataAutomationEngine()
    plan = engine.build_plan(
        "Join these files and create a scheduled pipeline with a diagram",
        [Path("a.csv"), Path("b.csv")],
    )
    assert "join" in plan.operations
    assert "pipeline" in plan.operations
    assert "diagram" in plan.operations


def test_generate_pipeline_diagram(tmp_path: Path) -> None:
    engine = DataAutomationEngine()
    pipeline = {
        "steps": [
            {"type": "read_csv", "path": "input.csv"},
            {"type": "write_csv", "path": "output.csv"},
        ]
    }
    pipeline_path = tmp_path / "pipeline.json"
    pipeline_path.write_text(json.dumps(pipeline))

    output_path = tmp_path / "pipeline.mmd"
    engine.generate_pipeline_diagram(pipeline_path, output_path)

    text = output_path.read_text()
    assert "flowchart TD" in text
    assert "S1 --> S2" in text


def test_profile_file(tmp_path: Path) -> None:
    engine = DataAutomationEngine()
    path = tmp_path / "data.csv"
    path.write_text("id,value\n1,3\n2,4\n")

    profile = engine.profile_file(path)
    assert profile["rows"] == 2
    assert profile["columns"] == 2
