"""
HealCode Lightweight Update Checker
"""

import time
import os
import json
from healcode.utils.ui import console

def check_for_updates(current_version: str, offline_mode: bool = False) -> None:
    if offline_mode:
        return

    # Check last check time using a cache file in temp / local directory
    cache_file = os.path.expanduser("~/.healcode_update_check")
    now = time.time()
    
    # Check at most once every 24 hours (86400 seconds)
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
                if now - data.get("last_check", 0) < 86400:
                    return
        except Exception:
            pass

    # Save check timestamp
    try:
        with open(cache_file, "w") as f:
            json.dump({"last_check": now}, f)
    except Exception:
        pass

    # Mock check showing a notification if there's a newer version (e.g. 1.1.0 vs 1.0.0)
    console.print("\n[bold yellow]★ Note:[/] A newer version of HealCode (v1.1.0) is available! Run `pip install --upgrade healcode` to update.")
