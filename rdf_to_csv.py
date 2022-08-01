#import dependencies 
import datetime
import csv
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, SKOS, DCTERMS 
import urllib.parse
from csv import DictReader
import uuid
import hashlib
import pandas as pd

#Find file path 
path = 'example.csv'

#establish empty lists for the IRIs we'll create 
iri_list = []

#load the csv file into a dataframe and display the first five rows 
ds = pd.read_csv(path)
ds.head()

#assigning columns to variables that we will loop through below 
resource_index = ds['Index']
resource_name = ds['Name']

#loop through instances to create unique IRIs for every instance in the csv file 
if __name__ == "__main__":
    for i in resource_index:
        seed = "index-" + str(i)
        m = hashlib.md5()
        m.update(seed.encode('utf-8'))
        guid = uuid.UUID(m.hexdigest(), version=5)
        iri_list.append('https://example.com/' + str(guid))

#adding columns to the dataframe to hold our newly generated IRIs 
ds['IRI'] = iri_list
ds.head()

#send finished dataframe back to csv path 
ds.to_csv(path)

df = csv.DictReader(open(path))

#establish prefix abbreviations  
CCO = Namespace('http://www.ontologyrepository.com/CommonCoreOntologies/')

#bind a prefix to a namespace URI 
g = Graph()
g.bind('cco', CCO)

for row in df:
    row = dict(row) 

    resource_iri = URIRef(row['IRI'])
    name = Literal(urllib.parse.quote(row['Name']), lang='en')
    latitude_value = Literal(row['Latitude'], datatype=XSD.float)
    longitude_value = Literal(row['Longitude'], datatype=XSD.float)
    port_index = Literal(row['Index'], datatype=XSD.int)
    created = Literal(datetime.datetime.now()) 

    g.add((resource_iri, RDF.type, OWL.NamedIndividual)) 
    g.add((resource_iri, RDF.type, CCO.Port))
    g.add((resource_iri, SKOS.prefLabel, name))
    g.add((resource_iri, RDFS.label, name))
    g.add((resource_iri, DCTERMS.created, created))
    g.add((resource_iri, CCO['has_latitude_value'], latitude_value))
    g.add((resource_iri, CCO['has_longitude_value'], longitude_value))
    g.add((resource_iri, DCTERMS.creator, Literal('USER NAME')))

#serialize and output to a specific path 

g.serialize(destination='USER PATH', format='turtle')

prepend = '<https://example.com>\n\ta owl:Ontology ;\n\tdcterms:title "Example"@en ;\n\tdcterms:created ""^^xsd:dateTime ;\n\towl:versionInfo "1.0.0" ;\n\tdcterms:description ""@en ;\n\towl:imports\n\t\t<http://www.ontologyrepository.com/CommonCoreOntologies/> ,\n\t\t'; + '\n\tdcterms:creator USER NAME ;\n\t;\n\t.\n\n'  

with open('USER PATH', 'r') as filename: 
    text = filename.readlines()
    text.insert(11,prepend)

with open('USER PATH', 'w') as filename:
    text = "".join(text)
    filename.write(text)