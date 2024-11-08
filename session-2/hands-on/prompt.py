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
For instance, question: What is the mascot of Georgetown University? The following is the query. 
```
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
SELECT ?mascot ?mascotLabel
WHERE {{
    wd:Q333886 wdt:P822 ?mascot .
    SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en"
    }}
}}
The ENTITIES and RELATIONS provided are 
ENTITIES: [{{'URI': 'http://www.wikidata.org/entity/Q333886', 'about': 'Georgetown University - private university in Washington, D.C., United States'}}, {{'URI': 'http://www.wikidata.org/entity/Q333886', 'about': 'Georgetown University - private university in Washington, D.C., United States'}}, {{'URI': 'http://www.wikidata.org/entity/Q5547055', 'about': 'MedStar Georgetown University Hospital - hospital in Washington, D.C.'}}]
RELATIONS: [{{'URI': 'http://www.wikidata.org/entity/P822', 'about': 'mascot - mascot of an organization, e.g. a sports team or university'}}, {{'URI': 'http://www.wikidata.org/entity/P7033', 'about': 'Australian Educational Vocabulary ID - ID for curriculum term in one of the controlled vocabularies at Australian education vocabularies'}}]
Identify the Entity:
From the entities provided, Q333886 (Georgetown University) is chosen because it directly corresponds to the question.

Select the Relation:
From the relations provided, P822 (mascot) is selected as it is relevant to finding the mascot of an organization like a university.

Construct the Query:
The query specifies that for entity Q333886, retrieve the value associated with property P822 (mascot) and assign it to the variable ?mascot.

Add Labels for Readability:
The SERVICE wikibase:label block fetches the name of the mascot in a readable format, in English or the user's language.

Output:
The query returns the mascot entity and its readable label, effectively answering the question.
```

For instance, question: Is the wingspan of the Andean Condor equal to 3.048?
```
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
ASK WHERE {{ wd:Q170598 wdt:P2050 ?obj filter(?obj = 3.048) }} 
```
ENTITIES: [{{'URI': 'http://www.wikidata.org/entity/Q36171706', 'about': 'Repeated conservation threats across the Americas: High levels of blood and bone lead in the Andean Condor widen the problem to a continental scale - scientific article'}}]
RELATIONS: [{{'URI': 'http://www.wikidata.org/entity/P2050', 'about': 'wingspan - distance from one wingtip to the other, of an airplane or an animal'}}]
Here’s a step-by-step explanation for the query:

Identify the Entity:
The entity Q170598 represents the Andean Condor, so the query focuses on information about this bird.

Select the Relation:
The property P2050 (wingspan) is used to retrieve the wingspan of the Andean Condor.

Construct the Query:
The query checks whether the wingspan value (?obj) of the Andean Condor matches 3.048 (meters).

Use ASK Query Type:
The ASK query type returns a true or false result, depending on whether the specified condition is satisfied.

Output:
The query will return:

true if the wingspan of the Andean Condor is indeed 3.048 meters.
false otherwise.
This query directly answers the question by verifying if the given wingspan value matches the specified number.

Instructions:
1.Identify the type of query it closely resembles by useing the above two examples.
2.Construct the query by only using the entites given in ENTITIES and realtions given in RELATIONS from the Schema. In case of multiple entites and relations use what is the closest. But use only one each.Donot use any other information to build the query. Please donot include the word QUERY in the final query
3.Also, ensure to include the two lines of the query which ensures that the answer is in human readable form and also is in english at all times.
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
MOST IMPORTANT: ONLY USE INFORAMTION FROM "Information" KEY above to answer and include all the information from the "Information" KEY
Helpful Answer:"""
SPARQL_QA_PROMPT = PromptTemplate(
    input_variables=["context", "prompt"], template=SPARQL_QA_TEMPLATE
)

