__author__ = "marc"

import requests
import json
import urllib
from Analyzers import HyperLink, DbpediaLink


def process_tdh_api(text):
    url = "http://entityclassifier.eu/thd/api/v2/extraction?"
    lang = "en"
    content_format = "json"
    entity_types = ["ne", "ce"]
    priority_entity_linking = "true"
    api_key = read_api_key()
    link_matches = HyperLink.extract_all_url(text)

    initial_entities = []
    for entity_type in entity_types:
        request = "apikey=" + api_key + \
                  "&format=" + content_format + \
                  "&lang=" + lang + \
                  "&priority_entity_linking=" + priority_entity_linking + \
                  "&entity_type=" + entity_type

        try:
            entities = requests.post(url + request, urllib.quote_plus(text))
            entities = json.loads(entities.text)
        except:
            return []

        for entity in entities:
            possible_link = False
            for link_match in link_matches:
                if link_match["start"] <= entity["startOffset"] and link_match["end"] >= entity["endOffset"]:
                    possible_link = True

            if not possible_link:
                e = {
                    "label": entity["underlyingString"],
                    "startOffset": entity["startOffset"],
                    "endOffset": entity["endOffset"],
                    "confidence": None,
                    "provenance": "thd",
                    "types": []
                }

                types = []
                try:
                    for data_type in entity["types"]:
                        thd_type = {
                            "typeURI": data_type["typeURI"],
                            "typeLabel": data_type["typeLabel"],
                            "entityURI": data_type["entityURI"],
                            "confidence": data_type["salience"]["confidence"],
                            "wikiURI": DbpediaLink.get_english_wikipedia_link_from_english_resource(data_type["entityURI"]),
                        }
                        types.append(thd_type)

                    e["types"].append(types)
                except KeyError:
                    continue
                initial_entities.append(e)

    initial_entities = {v["label"]: v for v in initial_entities}.values()
    return initial_entities


def read_api_key():
    try:
        lines = [line.strip() for line in open('Config/tdh.cfg')]
        return lines[0]
    except:
        print "No tdh.cfg file found in /Config or no api key on the first line of the file."
        exit()