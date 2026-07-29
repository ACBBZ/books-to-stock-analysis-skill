import json
from pathlib import Path

from books_to_stock_analysis_skill.cli import main


SKILL = {
    "schema_version": "1.0",
    "identity": {"id": "simple", "name": "Simple", "version": "0.1.0"},
    "classification": {"type": "pattern", "intents": ["analyze"]},
    "applicability": {"markets": ["CN_A_SHARE"], "timeframes": {"primary": "1d"}},
    "data_contract": {"minimum_bars": 1, "fields": ["close"]},
    "rules": {"required": {"all": ["close > 10"]}},
    "provenance": {"book_id": "synthetic", "source_fidelity_score": 1.0},
}


def test_validate_skill_prints_identity(tmp_path: Path, capsys) -> None:
    skill_path = tmp_path / "skill.json"
    skill_path.write_text(json.dumps(SKILL), encoding="utf-8")
    assert main(["validate-skill", str(skill_path)]) == 0
    output = capsys.readouterr().out
    assert '"id": "simple"' in output


def test_evaluate_prints_structured_result(tmp_path: Path, capsys) -> None:
    skill_path = tmp_path / "skill.json"
    observation_path = tmp_path / "observation.json"
    skill_path.write_text(json.dumps(SKILL), encoding="utf-8")
    observation_path.write_text(json.dumps({"close": 11}), encoding="utf-8")
    assert main(["evaluate", str(skill_path), str(observation_path)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "matched"
