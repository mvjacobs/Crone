__author__ = 'marc'

from bs4 import BeautifulSoup
import re
import json
from SPARQLWrapper import SPARQLWrapper, JSON
from urllib2 import urlopen


def get_category_links(section_url):
    """Get all news names from newser top 100
    :param section_url: url to the top 100 page on newser
    :return: list of newssite names
    """
    html = urlopen(section_url).read()
    soup = BeautifulSoup(html, "lxml")
    links = soup.findAll("div", {"id": re.compile('_ContentPlaceHolder1_RepeaterLinks_.*')})
    news_names = [link.find("a").string for link in links]
    return news_names


def get_dbpedia_homepage(url):
    """Get additional dbpedia data
    Uses SPARQL with the DBPedia endpoint to query

    :param url: url to dbpedia resource
    :return: homepage url or None
    """
    results = get_sparql_data(url)

    homepage = [result['entity']['value'] for result in results
                if result['property']['value'] == u'http://xmlns.com/foaf/0.1/homepage']

    if not homepage:
        homepage = get_redirected_page(url)

    if isinstance(homepage, list) and len(homepage) > 0:
        homepage = homepage[0]

    return homepage


def get_redirected_page(url):
    """Get additional dbpedia data from redirect

    :param url: url to redirected dbpedia resource
    :return: homepage url or None
    """
    results = get_sparql_data(url)

    redirects = [result['entity']['value'] for result in results
                 if result['property']['value'] == u'http://dbpedia.org/ontology/wikiPageRedirects']

    if redirects and len(redirects) > 0:
        return get_dbpedia_homepage(redirects[0])


def get_sparql_data(dbpedia_page):
    """Get all rdf entities from a dbpedia resource

    :param dbpedia_page: name of the dbpedia resource
    :return: list with properties of the resource
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> " \
            "SELECT * WHERE {<%s> ?property ?entity}" % dbpedia_page
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]


def filter_url(url):
    """Filter a URL for http and www and slashes

    :param url: source url
    :return: filtered url
    """
    url = url.replace("http://", "")
    url = url.replace("www.", "")
    url = url.replace("/", "")
    return url


def create_news_top_100(newspages):
    """Create a list of top 100 urls from newser.com

    :param newspages: newspage names
    :return: list of ranked newspages with filtered urls
    """
    urls = []
    i = 1
    for newspage in newspages:
        news_url = get_dbpedia_homepage('http://dbpedia.org/resource/' + newspage.replace(" ", "_"))

        if news_url:
            news_url = filter_url(news_url)

        urls.append(
            {
                u'id': i,
                u'name': u'%s' % newspage,
                u'url': u'%s' % news_url
            }
        )
        i += 1

    return urls


def newserlist_to_json():
    """Convert newser.com top 100 list to json

    :return: newser.json file
    """
    links_list = get_category_links("http://www.newser.com/topsites.aspx")
    newserlist = create_news_top_100(links_list)

    with open('newser.json', 'w') as f:
        json.dump(newserlist, f, ensure_ascii=False)

def newserlist_all_to_json():
    """Convert newser.com top 100 list to json

    :return: newser.json file
    """
    links_list = get_category_links("http://www.newser.com/topsites.aspx?type=all")
    newserlist = create_news_top_100(links_list)

    with open('newser_all.json', 'w') as f:
        json.dump(newserlist, f, ensure_ascii=False)



newserlist_all_to_json()