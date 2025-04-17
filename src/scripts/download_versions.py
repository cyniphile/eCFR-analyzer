import requests
from utils import get_titles_list, get_project_root, BASE_URL

root = get_project_root()
RAW_VERSIONS_PATH = root / "data" / "title_changes"


if __name__ == "__main__":
    r = get_titles_list()
    for title in r["titles"]:
        title_number = title["number"]
        versions = f"/api/versioner/v1/versions/title-{title_number}.json"

        r = requests.get(BASE_URL + versions)
        # TODO: keep track of date downloaded
        if not RAW_VERSIONS_PATH.exists():
            RAW_VERSIONS_PATH.mkdir(parents=True)
        with open(RAW_VERSIONS_PATH / f"title_{title_number}_changes.json", "w") as f:
            f.write(r.text)
