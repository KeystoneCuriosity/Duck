from SPARQLWrapper import SPARQLWrapper, JSON
from geopy.geocoders import Nominatim
import geonames.adapters.search
import json, urllib
import rdflib

geolocator = Nominatim()
_USERNAME = 'milossimic'
sa = geonames.adapters.search.Search(_USERNAME)

def get_country_description():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

    from SPARQLWrapper import SPARQLWrapper, JSON

#ABSTRACT
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
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

# url = 'http://api.geonames.org/search?q=Cuba&type=json&username=milossimic'

# response = urllib.urlopen(url)
# data = json.loads(response.read())
# print data['geonames'][0]['countryId']

# provinces = 'http://sws.geonames.org/3562981/contains.rdf'

# g = rdflib.Graph()
# g.parse(provinces)

# qres = g.query(
# 	"""
# 	PREFIX gn:<http://www.geonames.org/ontology#>
# 	SELECT ?name
# 	WHERE {?x gn:name ?name}""")

# for q in qres:
# 	print q[0]