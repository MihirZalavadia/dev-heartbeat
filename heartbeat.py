import json
import random
import os
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("data/daily_heartbeat.md")
STATE_FILE = Path("data/state.json")
LAST_FILE = Path("data/last_entry.json")

MIN_PER_DAY = 3
MAX_PER_DAY = 10

FORCE = os.getenv("FORCE_COMMIT") == "1"

THEMES = {
    "DOCKER": [
        "Optimized Dockerfile layers",
        "Rebuilt container image with slimmer base",
        "Validated container startup behavior",
    ],
    "CI-CD": [
        "Refined GitHub Actions workflow",
        "Tested scheduled CI execution",
        "Improved commit automation logic",
    ],
    "LINUX": [
        "Practiced log inspection using journalctl",
        "Checked open ports and firewall rules",
        "Reviewed systemd service lifecycle",
    ],
    "CLOUD": [
        "Reviewed Azure VM networking basics",
        "Revisited IAM and access boundaries",
        "Looked into cloud cost optimization patterns",
    ],
    "DEVOPS": [
        "Reviewed monitoring vs alerting strategy",
        "Reinforced infra-as-code concepts",
        "Studied deployment reliability patterns",
    ],
}

def utc_today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default

def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")

def ensure_log_header():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.write_text(
            "# 🫀 Daily Dev Heartbeat\n\n"
            "Short daily engineering logs generated via GitHub Actions.\n\n",
            encoding="utf-8",
        )

def main():
    today = utc_today()
    state = load_json(STATE_FILE, {})

    if state.get("date") != today:
        state = {
            "date": today,
            "target": random.randint(MIN_PER_DAY, MAX_PER_DAY),
            "count": 0,
        }

    if state["count"] >= state["target"]:
        save_json(STATE_FILE, state)
        return

    hour = int(datetime.now(timezone.utc).strftime("%H"))
    remaining_slots = max(1, 24 - hour)
    remaining_commits = state["target"] - state["count"]
    p = min(0.8, remaining_commits / remaining_slots)

    if not FORCE and random.random() > p:
        save_json(STATE_FILE, state)
        return

    theme = random.choice(list(THEMES.keys()))
    action = random.choice(THEMES[theme])

    ensure_log_header()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    line = f"- 🔧 **{theme}** | {action} ({now})\n"
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

    state["count"] += 1
    save_json(STATE_FILE, state)

    # Save last entry for commit message
    save_json(LAST_FILE, {"theme": theme, "action": action, "timestamp": now})

if __name__ == "__main__":
    main()
