from pathlib import Path

        from src.monitoring.healthcheck import check_config_files


        def test_check_config_files_detects_missing_file(tmp_path: Path) -> None:
            required = [
                "config/app.settings.yaml",
                "config/risk.limits.yaml",
                "config/alerts.yaml",
                "config/brokers/paper.yaml",
                "config/brokers/live.yaml",
            ]
            for relative in required[:-1]:
                target = tmp_path / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("ok: true
", encoding="utf-8")

            results = check_config_files(tmp_path)
            failed = [item for item in results if item["status"] == "fail"]

            assert len(failed) == 1
            assert failed[0]["name"] == "config/brokers/live.yaml"
