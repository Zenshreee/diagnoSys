import requests
import json

api_key = "f3143706-dfde-4745-8138-6d43614be53b"

endpoint = "https://www.dictionaryapi.com/api/v3/references/medical/json/{word}?key={api_key}"

def query_merriam_webster(word):
    """
    Querying Merriam-Webster API for a given medical term and returning the definition.
    """
    response = requests.get(endpoint.format(word=word, api_key=api_key))
    if response.status_code == 200:
        data = response.json()
        # taking only first definition
        if data:
            return data[0].get('shortdef', ['No definition found'])[0]
    return "Word not found."


def process_documents(documents):
    """
    Fetch definitions for each word in `reactionmeddrapt` entries.
    """
    definitions = {}  
    
    for doc in documents:
        for result in doc.get("results", []):
            for reaction in result.get("patient", {}).get("reaction", []):
                reaction_phrase = reaction.get("reactionmeddrapt", "")
                words = reaction_phrase.split()
                for word in words:
                    if word not in definitions:  # Avoid repeating API calls for the same word
                        definitions[word] = query_merriam_webster(word)
    
    return definitions

