__author__ = 'marc'

from SPARQLWrapper import SPARQLWrapper, JSON


def get_english_resource_from_english_wikipedia_link(english_wikipedia_link):
    try:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("SELECT * WHERE { ?resource foaf:isPrimaryTopicOf <" + english_wikipedia_link + "> .}")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except:
        return None

    if len(results['results']['bindings']) > 0:
        return results['results']['bindings'][0]['resource']['value']
    else:
        return None


def get_english_wikipedia_link_from_english_resource(resource):
    try:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("SELECT ?wikipedia WHERE {<" + resource + "> foaf:isPrimaryTopicOf ?wikipedia}")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except:
        return None

    if len(results['results']['bindings']) > 0:
        return results['results']['bindings'][0]['wikipedia']['value']
    else:
        return None
