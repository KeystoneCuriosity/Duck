from SPARQLWrapper import SPARQLWrapper, JSON
import geopy.geocoders
import json, urllib, urllib2
from xml.dom import minidom
import logging
import rdflib
from rdflib import Namespace,BNode
from rdflib import Graph, URIRef

def lookupDBpedia(country):
    url = "http://lookup.dbpedia.org/api/search.asmx/PrefixSearch?QueryClass=&MaxHits=5000&QueryString=" + country
    usock = urllib2.urlopen(url)
    xmldoc = minidom.parse(usock)
    # print url

    usock = urllib2.urlopen(url)
    xmldoc = minidom.parse(usock)

    for element in xmldoc.getElementsByTagName('Result'):
        label = element.getElementsByTagName('Label')[0].firstChild.nodeValue
        if 'hurricane' in label:
            url = element.getElementsByTagName('URI')[0].firstChild.nodeValue
            print label + " " + url

def getDBPedia(url):
    print 'parsing dbpedia for ' + url
    g = Graph()
    g.parse(url)

    # for predicate in g:
    #     if "property" in predicate:
    #         print predicate

    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    # seeAlso, affected, areasOf
    for s, _, dbpediaResource in g.triples((None, RDFS['seeAlso'], None)):
        if ('hurricane' in dbpediaResource) or ('Hurricane' in dbpediaResource):
            print dbpediaResource
    # for stmt in g.subject_objects(URIRef("http://dbpedia.org/property/affected")):
    #     print stmt

# def getDBPediaHurricane():

def parseGeoNameXML(url):
    usock = urllib2.urlopen(url)
    xmldoc = minidom.parse(usock)
    for element in xmldoc.getElementsByTagName('geoname'):
        toponymName = element.getElementsByTagName('toponymName')[0].firstChild.nodeValue
        print toponymName
        lookupDBpedia(toponymName)

def get_geonames(searchQuery):
    url = 'http://api.geonames.org/search?q={}&featureCode=ADM1&type=json&username=slivkaje'.format(searchQuery);
    print 'searching geoNames: ' + url
    # TODO: Moze biti i country ali ne razumem koji kod da uzmem za to http://www.geonames.org/export/codes.html
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    # for geoname in data['geonames']: # TODO: vrati vise odgovora nego sto treba
    geoname = data['geonames'][0]
    geonameId = geoname['geonameId']

    print "--------------------------------------------------------------------------------------------"
    print "NEIGHBOURS"
    url = "http://api.geonames.org/neighbours?geonameId={}&username=slivkaje".format(geonameId);
    parseGeoNameXML(url);

    print "--------------------------------------------------------------------------------------------"
    print "CHILDREN"
    url = "http://api.geonames.org/children?geonameId={}&username=slivkaje".format(geonameId);
    parseGeoNameXML(url);

            # Get country with geoname
    # g = Graph()
    # url = "http://www.geonames.org/{}/about.rdf".format(geonameId)
    # g.parse(url)
    # RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    # for s, _, dbpediaResource in g.triples((None, RDFS['seeAlso'], None)):
    #     getDBPedia(dbpediaResource)


# TODO: logging?
# logging.basicConfig()
get_geonames('Florida')
# lookupDBpedia('Florida')