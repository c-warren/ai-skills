"""progress.py — per-track course ledger for cadence-tutor.

JSON ledger at <course_dir>/progress.json. Standard library only; no CLI
entry point — call functions via `python3 -c`.

Schema:
{
  "total_days": 20,
  "days": {
    "01": {"delivered": "2026-08-11", "topic": "...",
           "quiz_score": "4/5", "exercise_pass": true,
           "graded": "2026-08-12", "note": "..."}
  }
}

A day is "current" (next to deliver) if it has no "delivered" stamp.
A delivered day is "ungraded" if it has no "graded" stamp.
"""
import json, os, datetime

def _today():
    return datetime.date.today().isoformat()

def load(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"total_days": 20, "days": {}}

def _save(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=1, sort_keys=True)

def current_day(path):
    """Return the next day number (int) to deliver, or None if course done."""
    d = load(path)
    for n in range(1, d.get("total_days", 20) + 1):
        if "delivered" not in d["days"].get(f"{n:02d}", {}):
            return n
    return None

def ungraded_days(path):
    """Delivered-but-ungraded day numbers, ascending."""
    d = load(path)
    return [int(k) for k, v in sorted(d["days"].items())
            if "delivered" in v and "graded" not in v]

def mark_delivered(path, day, topic):
    d = load(path)
    entry = d["days"].setdefault(f"{int(day):02d}", {})
    entry["delivered"] = _today()
    entry["topic"] = topic
    _save(path, d)

def record_grade(path, day, quiz_score, exercise_pass, note=""):
    d = load(path)
    entry = d["days"].setdefault(f"{int(day):02d}", {})
    entry.update({"graded": _today(), "quiz_score": quiz_score,
                  "exercise_pass": bool(exercise_pass), "note": note})
    _save(path, d)

def status(path):
    """Human-readable one-line-per-day summary."""
    d = load(path)
    lines = []
    for k, v in sorted(d["days"].items()):
        grade = (f"quiz {v.get('quiz_score', '?')}, "
                 f"exercise {'PASS' if v.get('exercise_pass') else 'FAIL'}"
                 if "graded" in v else "ungraded")
        lines.append(f"day {k}: {v.get('topic', '?')} — delivered {v['delivered']}, {grade}")
    nxt = current_day(path)
    lines.append(f"next: day {nxt:02d}" if nxt else "course complete")
    return "\n".join(lines) if lines else "no progress yet"
