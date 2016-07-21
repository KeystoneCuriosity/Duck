from surf import *

store = Store(  reader='rdflib',
            writer='rdflib',
            rdflib_store = 'IOMemory')

#DB PEDIA RDF LINK
DB_PEDIA = "http://dbpedia.org/projects/{}"
RDF=".rdf"
session = Session(store)

#ENTER NAME AND FORM A PATH
testVar = raw_input("Hurricane name:")
hurricane_name = DB_PEDIA.format(testVar+RDF)

#PRINT :)
print hurricane_name

#store.load_triples(source=hurricane_name)