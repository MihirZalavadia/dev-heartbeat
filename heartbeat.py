import json
import random
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("data/daily_heartbeat.md")
STATE_FILE = Path("data/state.json")

MIN_PER_DAY = 3
MAX_PER_DAY = 10

def utc_today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

def ensure_log_header():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.write_text(
            "# 🫀 Daily Dev Heartbeat\n\n"
            "Auto-updated by GitHub Actions. Consistency > motivation.\n\n",
            encoding="utf-8",
        )

def main():
    today = utc_today()
    state = load_state()

    # reset daily state
    if state.get("date") != today:
        state = {
            "date": today,
            "target": random.randint(MIN_PER_DAY, MAX_PER_DAY),
            "count": 0,
        }

    # already done for today -> do nothing (no commit)
    if state["count"] >= state["target"]:
        save_state(state)
        return

    # Decide whether to write this hour.
    # Probability increases as day progresses (so we don't miss target).
    # There are 24 runs/day. Remaining slots vs remaining commits:
    remaining_commits = state["target"] - state["count"]

    # Estimate remaining hourly runs in the day (rough but fine)
    hour = int(datetime.now(timezone.utc).strftime("%H"))
    remaining_slots = max(1, 24 - hour)

    # Commit probability (cap at 0.8 to avoid burst spam)
    p = min(0.8, remaining_commits / remaining_slots)

    if random.random() > p:
        save_state(state)
        return  # no change -> no commit

    # Make a real change (append a line)
    ensure_log_header()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- ✅ heartbeat @ **{now}** (#{state['count']+1}/{state['target']})\n")

    state["count"] += 1
    save_state(state)

if __name__ == "__main__":
    main()
