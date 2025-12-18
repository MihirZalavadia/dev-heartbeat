# heartbeat.py
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("data/daily_heartbeat.md")


def main():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    if LOG_FILE.exists():
        content = LOG_FILE.read_text(encoding="utf-8")
    else:
        content = "# 🫀 Daily Dev Heartbeat\n\n"
        content += "Auto-generated log to prove I'm alive and building.\n\n"

    content += f"- ✅ Auto-update at **{now}**\n"
    LOG_FILE.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
