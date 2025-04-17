import requests
import os
import time
from utils import get_titles_list, BASE_URL, data_dir

RAW_TITLES_PATH = data_dir / "raw_title_xml"

# TODO: refactor as function
if __name__ == "__main__":
    # Find the root of the git repository
    # Find the ./data directory relative to the root of the git repo
    print(f"Data will be saved to { data_dir }")

    # list all titles
    tl = get_titles_list()
    titles = tl["titles"]

    # download all titles
    if not os.path.exists(data_dir):
        os.makedirs(RAW_TITLES_PATH)
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
