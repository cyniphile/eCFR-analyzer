import requests
import os
from pathlib import Path
import time


# TODO: make idempotent

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


if __name__ == "__main__":
    # Find the root of the git repository
    # Find the ./data directory relative to the root of the git repo
    git_root = get_project_root()
    data_dir = git_root / "data/raw_title_xml"
    print(f"Data will be saved to { data_dir }")

    # list all titles
    tl = get_titles_list()
    tlj = tl.json()
    titles = tlj["titles"]

    # download all titles
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    for title in titles:
        title_number = title["number"]
        date = title["up_to_date_as_of"]
        print(f"Downloading title {title_number} as of {date}")
        title_url = f"{BASE_URL}/api/versioner/v1/full/{date}/title-{title_number}.xml"
        start_time = time.time()
        response = requests.get(title_url)
        print(f"Downloaded title {title_number} in {time.time() - start_time:.2f} seconds")
        # TODO: encode date metadata somewhere, so different versions can be downloaded
        with open(f"{data_dir}/title_{title_number}.xml", "wb") as f:
            f.write(response.content)
