import requests
from pathlib import Path
import os
import json

BASE_URL = "https://www.ecfr.gov/"
TITLES_LIST_URL = f"{BASE_URL}/api/versioner/v1/titles"
AGENCIES_LIST_URL = f"{BASE_URL}/api/admin/v1/agencies.json"


def get_titles_list(url=TITLES_LIST_URL):
    """
    Get the list of titles from the ECFR API
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to get titles list: {response.status_code}")
    return response.json()


def get_or_load_titles_list():
    """
    Get the list of titles from the ECFR API or load it from a local file
    """
    # Check if the file exists
    if os.path.exists(app_data_dir / "titles.json"):
        with open(app_data_dir / "titles.json", "r") as f:
            return json.load(f)
    else:
        # If not, fetch it from the API and save it
        titles = get_titles_list()
        with open(app_data_dir / "titles.json", "w") as f:
            json.dump(titles, f)
        return titles


def get_project_root() -> Path:
    return Path(os.popen("git rev-parse --show-toplevel").read().strip())


data_dir = get_project_root() / "data/"
app_data_dir = get_project_root() / "app_data/"
