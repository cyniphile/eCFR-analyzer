import requests
from pathlib import Path
import os

BASE_URL = "https://www.ecfr.gov/"
TITLES_LIST_URL = f"{BASE_URL}/api/versioner/v1/titles"


def get_titles_list(url=TITLES_LIST_URL):
    """
    Get the list of titles from the ECFR API
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to get titles list: {response.status_code}")
    return response.json()


def get_project_root() -> Path:
    return Path(os.popen("git rev-parse --show-toplevel").read().strip())
