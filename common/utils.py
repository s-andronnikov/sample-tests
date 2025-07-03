import json
import os
import random
import string
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from config import base_settings


def generate_random_string(length: int = 10) -> str:
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_email(domain: str = "example.com") -> str:
    """Generate a random email address"""
    username = generate_random_string(8)
    return f"{username}@{domain}"


def wait_for(condition_func, timeout: int = 10, poll_frequency: float = 0.5) -> bool:
    """Wait for a condition to be true"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(poll_frequency)
    return False


def load_resource(resource_path: str) -> str:
    """Load a resource file content"""
    base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
    file_path = base_dir / "resources" / resource_path

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_json_resource(resource_path: str) -> Dict[str, Any]:
    """Load a JSON resource file"""
    content = load_resource(resource_path)
    return json.loads(content)


def save_json_resource(data: Dict[str, Any], resource_path: str) -> None:
    """Save data to a JSON resource file"""
    base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
    file_path = base_dir / "resources" / resource_path

    # Ensure directory exists
    file_path.parent.mkdir(exist_ok=True, parents=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def get_relative_date(days: int = 0, hours: int = 0, minutes: int = 0) -> datetime:
    """Get a datetime relative to now"""
    return datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object as string"""
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse a string into a datetime object"""
    return datetime.strptime(dt_str, format_str)
