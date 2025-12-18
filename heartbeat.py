from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("data/daily_heartbeat.md")

def main():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if not LOG_FILE.exists():
        LOG_FILE.write_text(
            "# 🫀 Daily Dev Heartbeat\n\n"
            "Auto-updated by GitHub Actions. Proof of consistent building.\n\n",
            encoding="utf-8",
        )

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- ✅ heartbeat @ **{now}**\n")

if __name__ == "__main__":
    main()
