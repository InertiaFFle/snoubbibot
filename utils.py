import datetime
import subprocess
import time
import os

start_time = time.time()

def get_utc_datetime():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def get_git_tag():
    try:
        tag = subprocess.check_output(["git", "describe", "--tags"], stderr=subprocess.STDOUT).strip().decode("utf-8")
        return tag if tag else None
    except subprocess.CalledProcessError:
        return None

def get_uptime():
    uptime_seconds = time.time() - start_time
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
