import requests
import re
def ask_question(text):
    url = 'https://labs.tib.eu/falcon/falcon2/api?mode=long&k=3'
    headers = {
        'Content-Type': 'application/json'
    }
    pattern = r'QUERY:\s*(.*)'
    match = re.search(pattern, text)
    query_text = match.group(1)
    data = {
        'text': query_text
    }
    
    response = requests.post(url, headers=headers, json=data)
    # Return the JSON response
    return response.json()