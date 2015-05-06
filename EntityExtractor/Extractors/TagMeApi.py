__author__ = "marc"

import requests
import json
import urllib
from Analyzers import HyperLink, DbpediaLink


def process_tagme_api(text):
    try:
        lang = "en"
        url = "http://tagme.di.unipi.it/tag?"
        include_categories = "true"
        include_all_spots = "true"
        api_key = read_api_key()
        link_matches = HyperLink.extract_all_url(text)

        request = "key=" + api_key + \
                  "&include_categories=" + include_categories + \
                  "&lang=" + lang + \
                  "&include_all_spots=" + include_all_spots + \
                  "&text=" + urllib.quote_plus(text)

        entities = requests.post(url + request)
        entities = json.loads(entities.text)
    except:
        return []

    initial_entities = []
    for entity in entities["annotations"]:
        possible_link = False
        for link_match in link_matches:
            if link_match["start"] <= entity["start"] and link_match["end"] >= entity["end"]:
                possible_link = True

        if not possible_link:
            e = {
                "label": entity["spot"],
                "startOffset": entity["start"],
                "endOffset": entity["end"],
                "confidence": entity["rho"],
                "provenance": "tagme",
                "types": []
            }

            types = []
            for data_type in entity["dbpedia_categories"]:
                wiki_url = "http://en.wikipedia.org/wiki/" + data_type.replace(" ", "_")
                dbpedia_type = {
                    "typeURI": None,
                    "typeLabel": data_type,
                    "entityURI": DbpediaLink.get_english_resource_from_english_wikipedia_link(wiki_url),
                    "confidence": None,
                    "wikiURI": wiki_url
                }
                types.append(dbpedia_type)

            e["types"].append(types)
            initial_entities.append(e)

    initial_entities = {v["label"]: v for v in initial_entities}.values()
    return initial_entities


def read_api_key():
    try:
        lines = [line.strip() for line in open('Config/tagme.cfg')]
        return lines[0]
    except:
        print "No tagme.cfg file found in /Config or no api key on the first line of the file."
        exit()