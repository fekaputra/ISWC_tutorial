import requests
from SPARQLWrapper import SPARQLWrapper, JSON
endpoint = 'https://query.wikidata.org/sparql'
def query_sparql(sparql_query):
    full_url = f"{endpoint}?query={requests.utils.quote(sparql_query)}"
    headers = {'Accept': 'application/sparql-results+json'}
    
    response = requests.get(full_url, headers=headers)
    response.raise_for_status()  # Check for HTTP errors
    return response.json()

def get_entity_details(entities):
    # Initialize the SPARQL endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    # Extract entity IDs
    entity_ids = " ".join(f"wd:{entity['URI'].split('/')[-1]}" for entity in entities)
    
    # SPARQL query to get labels and descriptions for the entities
    query = f"""
    SELECT ?entity ?entityLabel ?entityDescription WHERE {{
      VALUES ?entity {{ {entity_ids} }}
      OPTIONAL {{ ?entity rdfs:label ?entityLabel . FILTER(LANG(?entityLabel) = "en") }}
      OPTIONAL {{ ?entity schema:description ?entityDescription . FILTER(LANG(?entityDescription) = "en") }}
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    # Execute query and retrieve results
    results = sparql.query().convert()
    
    # Map results to a dictionary for easy access
    entity_info = {
        result['entity']['value']: {
            'label': result.get('entityLabel', {}).get('value', ''),
            'description': result.get('entityDescription', {}).get('value', '')
        }
        for result in results['results']['bindings']
    }
    
    # Process input entities and add 'about' key
    for entity in entities:
        uri = entity['URI']
        label = entity_info[uri].get('label', '')
        description = entity_info[uri].get('description', '')
        entity['about'] = f"{label} - {description}" if description else label
        del entity['surface form']
    
    return entities


def get_relation_details(relations):
    # Initialize the SPARQL endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    # Extract relation IDs (with 'P' prefix)
    relation_ids = " ".join(f"wd:{relation['URI'].split('/')[-1]}" for relation in relations)
    
    # SPARQL query to get labels and descriptions for the properties (relations)
    query = f"""
    SELECT ?property ?propertyLabel ?propertyDescription WHERE {{
      VALUES ?property {{ {relation_ids} }}
      OPTIONAL {{ ?property rdfs:label ?propertyLabel . FILTER(LANG(?propertyLabel) = "en") }}
      OPTIONAL {{ ?property schema:description ?propertyDescription . FILTER(LANG(?propertyDescription) = "en") }}
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    # Execute query and retrieve results
    results = sparql.query().convert()
    
    # Map results to a dictionary for easy access
    relation_info = {
        result['property']['value']: {
            'label': result.get('propertyLabel', {}).get('value', ''),
            'description': result.get('propertyDescription', {}).get('value', '')
        }
        for result in results['results']['bindings']
    }
    
    # Process input relations and add 'about' key
    for relation in relations:
        uri = relation['URI']
        label = relation_info[uri].get('label', '')
        description = relation_info[uri].get('description', '')
        relation['about'] = f"{label} - {description}" if description else label
        del relation['surface form']
    
    return relations
def extract_label_values(data):
    # Identify the label key dynamically from the 'vars' list in the 'head' section
    label_key = next((var for var in data['head']['vars'] if var.endswith('Label')), None)
    
    # Initialize an empty list to store the label values
    answer = []
    
    # Check if the label key exists
    if label_key:
        # Iterate over each binding in the results
        for item in data['results']['bindings']:
            # Check if the label key exists in the current item and add its value to the answer list
            if label_key in item:
                answer.append(item[label_key]['value'])
    
    return answer
#sparql_query = """
#SELECT ?birthPlace ?birthPlaceLabel ?birthPlaceDescription
#WHERE {
#    wd:Q76 wdt:P19 ?birthPlace .
#    SERVICE wikibase:label {
#      bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
#    }
#}
#"""
#
#results = query_sparql(endpoint_url, sparql_query)
#print(results)
#