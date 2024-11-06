# flake8: noqa
from langchain_core.prompts.prompt import PromptTemplate

SPARQL_INTENT_TEMPLATE = """Task: Identify the intent of a prompt and return the appropriate SPARQL query type.
You are an assistant that distinguishes different types of prompts and returns the corresponding SPARQL query types.
Consider only the following query types:
* SELECT: this query type corresponds to questions
* UPDATE: this query type corresponds to all requests for deleting, inserting, or changing triples
Note: Be as concise as possible.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that ask for anything else than for you to identify a SPARQL query type.
Do not include any unnecessary whitespaces or any text except the query type, i.e., either return 'SELECT' or 'UPDATE'.

The prompt is:
{prompt}
Helpful Answer:"""
SPARQL_INTENT_PROMPT = PromptTemplate(
    input_variables=["prompt"], template=SPARQL_INTENT_TEMPLATE
)

SPARQL_GENERATION_SELECT_TEMPLATE = """Task: Generate a SPARQL SELECT statement for querying a graph database.
For instance, question: Where was barak obama born?
For instance, question: What is the name of the Belgrade Airport ?
```
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
SELECT DISTINCT ?sbj ?sbjLabel WHERE {{
  ?sbj wdt:P931 wd:Q3711 .
  ?sbj wdt:P31 wd:Q1248784 .
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }}
}}
```
```
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
SELECT ?birthPlace ?birthPlaceLabel ?birthPlaceDescription
WHERE {{
    wd:Q76 wdt:P19 ?birthPlace .  # Retrieves the birthplace of Barack Obama
    SERVICE wikibase:label {{                  #This ensures that the answer is in human readable for at all times
      bd:serviceParam wikibase:language [AUTO_LANGUAGE],en"  # Ensures labels and descriptions are in English
    }}
}}
```

Instructions:
Construct the query by only using the entites given in ENTITIES and realtions given in RELATIONS from the Schema. In case of multiple entites and relations use what is the closest. But use only one each.Donot use any other information to build the query.
Also, ensure to include the two lines of the query whihc ensures that the answer is in human readable form and also is in english at all times.
Schema:
{schema}
Note: Be as concise as possible.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that ask for anything else than for you to construct a SPARQL query.
Do not include any text except the SPARQL query generated.
The question is:
{prompt}"""
SPARQL_GENERATION_SELECT_PROMPT = PromptTemplate(
    input_variables=["schema", "prompt"], template=SPARQL_GENERATION_SELECT_TEMPLATE
)

SPARQL_GENERATION_UPDATE_TEMPLATE = """Task: Generate a SPARQL UPDATE statement for updating a graph database.
For instance, to add 'jane.doe@foo.bar' as a new email address for Jane Doe, the following query in backticks would be suitable:
```
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
INSERT {{
    ?person foaf:mbox <mailto:jane.doe@foo.bar> .
}}
WHERE {{
    ?person foaf:name "Jane Doe" .
}}
```
Instructions:
Make the query as short as possible and avoid adding unnecessary triples.
Use only the node types and properties provided in the schema.
Do not use any node types and properties that are not explicitly provided.
Include all necessary prefixes.
Schema:
{schema}
Note: Be as concise as possible.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that ask for anything else than for you to construct a SPARQL query.
Return only the generated SPARQL query, nothing else.

The information to be inserted is:
{prompt}"""
SPARQL_GENERATION_UPDATE_PROMPT = PromptTemplate(
    input_variables=["schema", "prompt"], template=SPARQL_GENERATION_UPDATE_TEMPLATE
)

SPARQL_QA_TEMPLATE = """Task: Generate a natural language response from the results of a SPARQL query.
You are an assistant that creates well-written and human understandable answers.
The information part contains the information provided, which you can use to construct an answer.
The information provided is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make your response sound like the information is coming from an AI assistant, but don't add any information.
Information: 
{context}

Question: {prompt}
MOST IMPORTANT: ONLY USE INFORAMTION FROM "Information" KEY above, if it is empty, just say: SORRY
Helpful Answer:"""
SPARQL_QA_PROMPT = PromptTemplate(
    input_variables=["context", "prompt"], template=SPARQL_QA_TEMPLATE
)

