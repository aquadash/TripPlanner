import azure.functions as func
import logging
import json
import random
from typing import List
import os
import openai
from places import get_place_object, get_location_from_query, get_places_from_query, Place

import aoaidata

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OAI_ENDPOINT")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OAI_KEY")

def get_entities(query, sysms):

    user_input = query
    system_msg = sysms
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
    try:
        retry = int(req.params.get('retry'))
    except:
        retry = 0
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
            limit = req_body.get('limit',5)
    try:
        limit = int(limit)
    except:
        limit = 5
    
    # get locked places
    locked_places = []
    try:
        req_body = req.get_json()
    except ValueError:
        locked_places = []
    else:
        locked_places = req_body.get('locked_places',[])
    
    
    if query:
        try:
          
            system_msg_query = "You will be given a free text query from a user, containing information about their geographic location, what they are interested in doing in this location, and if they have a wheelchair accessibility requirement. You need to extract the geographic location, activities and accessibility requirements from the user-entered text. Return those as a well formatted json object, with the following keys: location, interests, wheelchair_accessibility_requirements. wheelchair_accessibility_requirements should be a boolean value"
            entities:dict = get_entities(query, system_msg_query)
            if not entities.get("location"):
                # set to adelaide if no location given
                location = {'lat': -34.9284989, 'lng': 138.6007456}
            else:
                location: dict = get_location_from_query(entities["location"])
            places: List[str] = get_places_from_query(entities["interests"], location)
              # jostep stuff - fix and intergreate
              #ragsearch = aoaidata.conversation_with_data(query, entities)
              #   recommendations = ragsearch.get('choices')[0].get('messages')[1].get('content')
              #   finalrec = get_entities("Extract top 5 places from each list and return as a non-numbered list. Choose a diverse set and respond with the list and nothing else", recommendations)

            # Add locked places to place list
            # if locked_places and len(locked_places)>0:
            #     locked_place_objects = [get_place_object(place).to_dict() for place in locked_places]
            # else:
            #     locked_place_objects = []
            # #places = places[:limit] # TODO there is an edge case here where a locked card could have a higher index than the limit and be excluded

            place_objects: List[Place] = [get_place_object(place).to_dict() for place in places]

            # ensure wheelchair accessibility
            if entities["wheelchair_accessibility_requirements"]:
                place_objects = [place for place in place_objects if place["wheelchair_accessible_entrance"] == True]

            # rank places
            if retry == 1:
                place_objects = place_objects[5:10]
            else:
                place_objects = place_objects[:limit]
            ranked_places = rank_places(query, place_objects)
            for place in ranked_places:
                place_object = next((x for x in place_objects if x["id"] == place["place_id"]), None)
                if place_object:
                    place_object["score"] = place["score"] # add score to place object
                    place_object["description"] = place["description"] # give a custom description
                else:
                    logging.info(f"Place not found. {place['place_id']}")
            
            place_objects.sort(key=lambda x: x["score"], reverse=True)

            return_object = {
                "description": "This is a summary of the results",
                "places": place_objects[:limit],
                "ranked_places": ranked_places,
                "retry": retry,
            }
            return func.HttpResponse(json.dumps(return_object), mimetype="application/json",status_code=200)
        except Exception as e:
            logging.error(e)
            return func.HttpResponse(
                 f"Error: {e}",
                 status_code=400
            )

    else:
        return func.HttpResponse(
             "Please pass a query on the query string or in the request body. Example: govhack-tripplanner.azurewebsites.net/api/places?query='test'",
             status_code=400
        )
    
