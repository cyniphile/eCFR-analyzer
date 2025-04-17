import requests
from lxml import etree
import re
from utils import AGENCIES_LIST_URL
import json
import pandas as pd

from utils import data_dir


def word_count_sans_xml(xml_string):
    """
    Strip XML tags from a document using regex and count words.

    Args:
        xml_string (str): The XML content as a string

    Returns:
        str: Plain text with XML tags removed
        int: Word count
    """
    # Remove all XML tags
    text_only = re.sub(r"<[^>]+>", " ", xml_string)

    # Clean up whitespace (multiple spaces, newlines, etc.)
    clean_text = re.sub(r"\s+", " ", text_only).strip()

    # Count words
    word_count = len(clean_text.split())

    return word_count


# Parse the XML


def get_word_count_for_agency(agency_references_json):
    word_count = 0
    for json_path in agency_references_json:
        title_number = json_path["title"]
        with open(data_dir / f"raw_title_xml/title_{title_number}.xml", "r") as f:
            xml_string = f.read()
        parser = etree.XMLParser(recover=True)  # More forgiving parser
        root = etree.fromstring(xml_string.encode("utf-8"), parser)
        for k, v in json_path.items():
            if k == "title":
                continue
            element = XML_DOCUMENT_SCHEMA_MAP[k]["element"]
            type = XML_DOCUMENT_SCHEMA_MAP[k]["type"]
            # Find the part (DIV5)
            xpath = f".//{element}[@N='{v}']"
            elements = root.xpath(xpath)
            if len(elements) == 0:
                print(f"Element not found: {xpath}")
                continue
            if len(elements) > 1:
                print(f"Multiple elements found: {xpath}")
                continue
            element = elements[0]
            root = element

        # Convert the element back to string
        s = etree.tostring(root, encoding="unicode", pretty_print=True)
        word_count += word_count_sans_xml(s)
    return word_count


if __name__ == "__main__":
    AGENCIES_PATH = "/api/admin/v1/agencies.json"
    r = requests.get(AGENCIES_LIST_URL)
    agencies = r.json()["agencies"]
    agencies_filename = data_dir / "agencies.json"

    with open(agencies_filename, "w") as f:
        json.dump(agencies, f, indent=4)

    df = pd.read_json(agencies_filename)

    # Check the structure of the cfr_references column to determine which section types can be used
    # all = df["cfr_references"].to_list()
    # types = set()
    # for l in all:
    #     if isinstance(l, list):
    #         for d in l:
    #             for k, v in d.items():
    #                 types.add(k)
    #     else:
    #         for k, v in d.items():
    #             types.add(k)

    XML_DOCUMENT_SCHEMA_MAP = {
        "chapter": {"element": "DIV3", "type": "CHAPTER"},
        "part": {"element": "DIV5", "type": "PART"},
        "subchapter": {"element": "DIV4", "type": "SUBCHAP"},
        "subtitle": {"element": "DIV2", "type": "SUBTITLE"},
    }
    # Assuming this is pretty well formed data. Two agencies don't point to the same data, there is no orphaned data, etc.
    child_dfs = []
    for i, row in df.iterrows():
        agency = row["name"]
        children_df = pd.DataFrame(row["children"])
        if len(children_df) > 0:
            children_df["parent_agency"] = agency
            child_dfs.append(children_df)

    child_dfs = pd.concat(child_dfs, ignore_index=True)
    df["parent_agency"] = df["name"]
    all_df = pd.concat([df, child_dfs], ignore_index=True)
    all_df["word_count"] = all_df["cfr_references"].apply(get_word_count_for_agency)
    all_df.to_csv(data_dir / "agencies_word_count.csv", index=False)
