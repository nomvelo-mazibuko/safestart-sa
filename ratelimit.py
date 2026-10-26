"""A very simple limit on how often the link checker can be used.

Everything is kept in the computer's memory only, so nothing personal is stored
and the counters reset when the server restarts.
"""
import time

WINDOW_SECONDS = 600     
PER_VISITOR_MAX = 5      
EVERYONE_MAX = 60        

_history = {}  


def _recent_calls(name, now):
    """Return the list of recent checks for this name, with old ones removed."""
    calls = _history.get(name, [])
    recent = [t for t in calls if now - t < WINDOW_SECONDS]
    _history[name] = recent
    return recent


def check_and_record(visitor_id):
    """Return (allowed, message). If allowed, the check is counted."""
    now = time.time()
    mine = _recent_calls(visitor_id, now)
    everyone = _recent_calls("EVERYONE", now)

    if len(mine) >= PER_VISITOR_MAX:
        return False, "You have run several checks in a short time. Please wait a few minutes and try again."
    if len(everyone) >= EVERYONE_MAX:
        return False, "The checker is very busy right now. Please try again in a few minutes."

    mine.append(now)
    everyone.append(now)

    if len(_history) > 2000:
        for name in list(_history):
            if len(_history[name]) == 0:
                del _history[name]
    return True, ""
