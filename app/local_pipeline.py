import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class LocalDataPipeline:
    """File-backed stand-in for the GCS raw and BigQuery staged sinks."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.raw_path = data_dir / "d0_raw_landing.jsonl"
        self.staged_path = data_dir / "d1_staged.jsonl"

    def write_onboarding(self, payload: dict[str, Any]) -> dict[str, str]:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        record = {
            **payload,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._append_json_line(self.raw_path, record)
        self._append_json_line(self.staged_path, record)
        return {
            "raw_file": str(self.raw_path),
            "staged_file": str(self.staged_path),
        }

    @staticmethod
    def _append_json_line(path: Path, record: dict[str, Any]) -> None:
        with path.open("a", encoding="utf-8") as output_file:
            output_file.write(json.dumps(record) + "\n")
