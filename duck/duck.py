from SPARQLWrapper import SPARQLWrapper, JSON
from geopy.geocoders import Nominatim
import geonames.adapters.search
import json, urllib
import rdflib

geolocator = Nominatim()
_USERNAME = 'milossimic'
sa = geonames.adapters.search.Search(_USERNAME)
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

def get_country_description():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

    from SPARQLWrapper import SPARQLWrapper, JSON

#ABSTRACT
sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT ?abstract
    WHERE { <http://dbpedia.org/resource/Hurricane_Katrina> dbo:abstract ?abstract }
""")
sparql.setReturnFormat(JSON)
abstract = sparql.query().convert()

for a in abstract['results']['bindings']:
	if a['abstract']['xml:lang'] == 'en':
		print a['abstract']['value']

print
print

#COUNTRY AND PROVINCE LEVEL 1
sparql.setQuery("""
    PREFIX dbp: <http://dbpedia.org/property/>
    SELECT ?areas
    WHERE { <http://dbpedia.org/resource/Hurricane_Katrina> dbp:areas ?areas }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    for line in result["areas"]["value"].split(','):
		try:
			location = geolocator.geocode(line.strip())
			print(location.latitude, location.longitude), line.strip()

			url = 'http://api.geonames.org/search?q={}&type=json&username=milossimic'.format(line.strip())

			response = urllib.urlopen(url)
			data = json.loads(response.read())
			countryId = data['geonames'][0]['countryId']

			provinces = 'http://sws.geonames.org/{}/contains.rdf'.format(countryId)

			g = rdflib.Graph()
			g.parse(provinces)

			qres = g.query(
				"""
				PREFIX gn:<http://www.geonames.org/ontology#>
				SELECT ?name
				WHERE {?x gn:name ?name}""")

			for q in qres:
				print "\t",q[0]

			print

		except AttributeError:
			print line.strip()

#DEATH BY REGION AND SO ON TOTAL AMOUNT OF DAMANGE PREASSURE PEAK STRENGHT
sparql.setQuery("""
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?pressure ?damages ?1MinWinds ?isPrimaryTopicOf ?formed ?dissipated
    WHERE { 
    <http://dbpedia.org/resource/Hurricane_Katrina> dbp:pressure ?pressure.
    <http://dbpedia.org/resource/Hurricane_Katrina> dbp:damages ?damages.
    <http://dbpedia.org/resource/Hurricane_Katrina> dbp:1MinWinds ?1MinWinds. 	
    <http://dbpedia.org/resource/Hurricane_Katrina> foaf:isPrimaryTopicOf ?isPrimaryTopicOf.
    <http://dbpedia.org/resource/Hurricane_Katrina> dbp:formed ?formed.
    <http://dbpedia.org/resource/Hurricane_Katrina> dbp:dissipated ?dissipated.

    }
""")
sparql.setReturnFormat(JSON)
rest_of_it = sparql.query().convert()

main_data = rest_of_it['results']['bindings'][0]
pressure = main_data['pressure']['value']
isPrimaryTopicOf = main_data['isPrimaryTopicOf']['value']
damages = main_data['damages']['value']
wind = main_data['1MinWinds']['value']
formed = main_data['formed']['value']
dissipated = main_data['dissipated']['value']

print pressure, isPrimaryTopicOf, damages, wind, formed, dissipated










