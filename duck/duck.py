from SPARQLWrapper import SPARQLWrapper, JSON

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

print results