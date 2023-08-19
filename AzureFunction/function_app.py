import azure.functions as func
import logging
import json
from typing import List
import os
import openai 
from dotenv import load_dotenv
from places import get_place_object, get_location_from_query, get_places_from_query, Place
load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OAI_ENDPOINT")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OAI_KEY")


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# class AccessibilityFeature:
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description
    
#     def __str__(self):
#         return {self.name: self.description}
#     def __repr__(self):
#         return {self.name: self.description}


def get_sample_data():
    with open("sample_find_places.json", "r") as f:
        data = json.load(f)
    places = []
    for place in data["results"]:
        places.append(Place.from_json(place).to_dict())
    return places

def get_entities(query):

    user_input = query
    #system_msg = "A user will tell you where they want to go (geographical location), what accessibility requirements they have and what they want to do (in free text form). You need to extract the geographic location, activites and accessibility requirements (they might give multiple places, activities or accessibility requirements. Extract all of those, no hyphens, and return only one key word for each, e.g. wheelchair instead of wheelchair access. Also make all words singular form.) from user-entered text. Return those as json"
    system_msg = "You will be given a free text query from a user, containing information about their geographic location, what they are interested in doing in this location, and their accessibility requirements. You need to extract the geographic location, activities and accessibility requirements from the user-entered text. Return those as a well formatted json object, with the following keys: location, interests, accessibility_requirements."
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
    engine="gpt-4",
    messages = messages,
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None)

    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages = messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    extracted_activities = response.choices[0].message['content']

    return json.loads(extracted_activities)
        

@app.route(route="places", methods=["GET"])
def Places(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('query')
    
    if query:
        entities = get_entities(query)
        location: dict = get_location_from_query(entities["location"])
        places: List[str] = get_places_from_query(entities["interests"], location)
        place_objects: List[Place] = [get_place_object(place).to_dict() for place in places]
        # 1. process query
        # 1.1 Open AI query - get location, interests, etc.

        # 2. Search for places
        # 2.1 Call places API with search parameters
        # 2.2 Get places from API
        # 2.3 Look for places from other data sources?

        # 3. Filter places based on query
        # not sure the best way to do this 

        # 4. Format and return places
        # 4.1 Call place details API for filtered places to get more details
        # 4.2 Format places into places class (needs modification, it's above)
        # 4.3 Return places as JSON
        # print(get_entities(query))
        return_object = {
        "places": place_objects,
        }
        return func.HttpResponse(json.dumps(return_object), mimetype="application/json",status_code=200)
    else:
        return func.HttpResponse(
             "Please pass a query on the query string or in the request body. Example: govhack-tripplanner.azurewebsites.net/api/places?query='test'",
             status_code=400
        )
    
