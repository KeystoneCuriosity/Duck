from SPARQLWrapper import SPARQLWrapper, JSON
from geopy.geocoders import Nominatim

geolocator = Nominatim()

def get_country_description():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

    from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
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
		except AttributeError:
			print line.strip()