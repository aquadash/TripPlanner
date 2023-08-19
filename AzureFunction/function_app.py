import azure.functions as func
import logging
import json
from typing import List
import os
import openai
from AzureFunction.places import get_place_object, get_location_from_query, get_places_from_query, Place

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OAI_ENDPOINT")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OAI_KEY")

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
        stop=None
    )
    extracted_activities = response.choices[0].message['content']

    return json.loads(extracted_activities)

def rank_places(query:str, places: List[Place]):
    system_message = """You will be given a user query within the <query> tag, and multiple places within the <places> tag. 
    You need to rank the places based on how well they match the user query. 
    Each place will be contained within a <place> tag.
    You are to return a well formatted json object, with a "places" list containing: place_id, description, and a score.
    The place_id should be the place_id of the place, the description should be a short description of why the the place would be interesting for the user, and the score should be a number between 0 and 1, with 1 being the best match and 0 being the worst match.
    Example response:
    {
        "places": [
            {"place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4", "description": "This coffee shop has a high rating, and is close to your areas of interest.", "score": 0.9},
            {"place_id": "ChIJF1k2tdXOsGoRKq4uZzLQMtg", "description": "This musuem is open now. The 5-floor building is devoted to natural history artifacts which you mentioned you liked", "score": 0.9},
        ]
    }
    """
    template_place_string = "<place id={id}> <name>{name}</name> <description>{description}</description> <rating>{rating}</rating> <num_ratings>{num_ratings}</num_ratings></place>"
    places = "\n".join([template_place_string.format(id=place['id'], name=place['name'], description=place['description'], rating=place['rating'], num_ratings=place['numRatings']) for place in places])
    user_query = "<query>{query}</query>\n<places>{places}</places>".format(query=query, places=places)
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_query}
    ]
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
    rankings = response.choices[0].message['content']
    try:
        result = json.loads(rankings)
        sorted_places = sorted(result["places"], key=lambda x: x["score"], reverse=True)
    except:
        sorted_places = [] # case when json object fails to parse
    return sorted_places


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="places", methods=["GET"])
def Places(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # get query
    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('query')

    # limit api results
    limit = req.params.get('limit')
    if not limit:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            limit = req_body.get('limit',10)
    try:
        limit = int(limit)
    except:
        limit = 10
    
    # get locked places
    try:
        req_body = req.get_json()
    except ValueError:
        locked_places = []
    else:
        locked_places = req_body.get('locked_places',[])
    
    
    if query:
        entities = get_entities(query)
        location: dict = get_location_from_query(entities["location"])
        places: List[str] = get_places_from_query(entities["interests"], location)
        

        # Add locked places to place list
        if len(locked_places)>0:
            locked_place_objects = [get_place_object(place).to_dict() for place in locked_places]
            locked_places.sort(key=lambda x: x[1])
            for place_id, idx in locked_places:
                places.insert(idx, (place_id, "No name stored"))
        #places = places[:limit] # TODO there is an edge case here where a locked card could have a higher index than the limit and be excluded

        place_objects: List[Place] = [get_place_object(place).to_dict() for place in places]

        # rank places
        ranked_places = rank_places(query, place_objects)

        for place in ranked_places:
            place_object = next((x for x in place_objects if x["id"] == place["place_id"]), None)
            if place_object:
                place_object["score"] = place["score"] # add score to place object
                place_object["description"] = place["description"] # give a custom description
            else:
                print("Place not found")
                pass
        
        place_objects.sort(key=lambda x: x["score"], reverse=True)
        place_objects = place_objects[:limit]
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
            "description": "This is a summary of the results",
            "places": place_objects, 
        }
        return func.HttpResponse(json.dumps(return_object), mimetype="application/json",status_code=200)
    else:
        return func.HttpResponse(
             "Please pass a query on the query string or in the request body. Example: govhack-tripplanner.azurewebsites.net/api/places?query='test'",
             status_code=400
        )
    
